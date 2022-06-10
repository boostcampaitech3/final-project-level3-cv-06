import uvicorn

from typing import Optional
from fastapi import FastAPI
from dataclasses import asdict
from starlette.middleware.cors import CORSMiddleware
from app.database.conn import db
from app.common.config import conf
from app.router import img, auth


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
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=30004)

# TODO: 유저의 이미지를 받아서 inference하는 함수 -> 디비에 예측 결과, bbox 정보 저장
# TODO: 이전에 찍은 사진 이미지를 가져와서 시각화(비교)해주는 함수(이전, 현재) 날짜를 보내면 되나?
# TODO: 전체 가져오기(한번에 5개): get_all(order: descent, 최신순)
# TODO: 
# TODO:
# TODO:
# TODO: