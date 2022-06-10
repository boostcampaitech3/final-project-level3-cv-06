import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timedelta
from app.common.const import ALGORITHM, SECRET_KEY


class AuthHandler():
    security = HTTPBearer()
    secret_key = SECRET_KEY
    algorithm = ALGORITHM
    
    def encode_token(self, user_id):
        payload = {
            'exp': datetime.now() + timedelta(hours=1),
            'iat': datetime.now(),
            'sub': user_id
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=ALGORITHM)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="SIGNATURE HAS EXPIRED")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="INVALID TOKEN")
    
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)