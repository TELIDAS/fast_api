from datetime import datetime

from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    description: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    title: str
    description: str
    published: bool
    created_date: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_date: datetime


    class Config:
        orm_mode = True
