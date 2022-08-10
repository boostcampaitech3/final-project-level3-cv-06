from pydantic import BaseModel, Field
from pydantic.networks import EmailStr
from typing import List, Optional


class UserRegister(BaseModel):
    user_id: str
    password: str


class Login(BaseModel):
    user_id: str = None
    password: str = None

class ImageLoad(BaseModel):
    image_name: str = None


class UserJWT(BaseModel):
    id: int
    user_id: str = None
    
    class Config:
        orm_mode = True

