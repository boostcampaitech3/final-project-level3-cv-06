import uvicorn

from typing import Optional
from fastapi import FastAPI
from dataclasses import asdict
from starlette.middleware.cors import CORSMiddleware
from app.database.conn import db
from app.common.config import conf
from app.router import img, auth
from app.common.const import BACKEND_PORT

def create_app():
    c = conf()
    app = FastAPI()

    conf_dict = asdict(c)
    db.init_app(app, **conf_dict)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=conf().ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(img.router)
    

    return app


app = create_app()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=BACKEND_PORT)

