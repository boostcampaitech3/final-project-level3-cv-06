import jwt
import time
from decouple import config
from fastapi import HTTPException, Security
from starlette.responses import Response, JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from datetime import datetime, timedelta
from app.errors import exceptions
from app.database.schema import UserJWT
from app.utils.logger import api_logger
from app.service.auth_service import url_pattern_check


class AuthHandler():
    security = HTTPBearer()
    secret_key = config("SECRET_KEY")
    algorithm = config("ALGORITHM")
    
    def encode_token(self, user_info):
        payload = {
            'exp': datetime.now() + timedelta(hours=1),
            'iat': datetime.now(),
            'sub': user_info
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token):
        payload = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
        return payload['sub']

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)


class AuthRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.req_time = datetime.now()
        request.state.start = time.time()
        request.state.inspect = None
        request.state.user = None
        request.state.service = None
        headers = request.headers
        url = request.url.path
        error = None
        
        # AWS에서는 로드밸런서를 통하면서 x-forwarded-for가 생김
        ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
        request.state.ip = ip.split(",")[0] if "," in ip else ip
    
        if await url_pattern_check(url, config("EXCEPT_PATH_REGEX")) \
            or url in config("EXCEPT_PATH_LIST"):
            return await call_next(request)
        if request.method == "OPTIONS":
            return await call_next(request)
        
        if "authorization" not in headers.keys():
            error = exceptions.NotAuthorized()
            await api_logger(request=request, error=error)
            return JSONResponse(
                status_code=error.status_code,
                content=dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)                
            )
            
        try:
            token = headers.get("authorization").split(" ")[1].strip()
            token_info = AuthHandler().decode_token(token)
            request.state.user = UserJWT(**token_info)
            response = await call_next(request)
            await api_logger(request=request, response=response)
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError
        ) as e:
            if e == jwt.ExpiredSignatureError:
                error = exceptions.TokenExpiredEx()
            else:
                error = exceptions.TokenDecodeEx()
            error_dict = dict(status=error.status_code, msg=error.msg, detail=error.detail, code=error.code)
            
            response = JSONResponse(
                status_code=error.status_code,
                content=error_dict
            )
            await api_logger(request=request, error=error)

        return response