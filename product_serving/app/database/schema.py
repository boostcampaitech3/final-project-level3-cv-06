from pydantic import BaseModel, Field
from typing import List, Optional


class UserRegister(BaseModel):
    user_id: str
    password: str


class Login(BaseModel):
    user_id: str = None
    password: str = None

class ImageLoad(BaseModel):
    image_name: str = None



