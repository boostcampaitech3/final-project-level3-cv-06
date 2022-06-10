from dataclasses import dataclass, asdict
from os import environ
from pathlib import Path
from app.common.const import DB_URL

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    BASE_DIR = BASE_DIR
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True
    DB_URL: str = DB_URL  # DB 주소
    ALLOW_SITE = ["*"]

@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    config = dict(prod=ProdConfig(), local=LocalConfig())
    print(config)
    return config.get(environ.get("API_ENV", "local"))




