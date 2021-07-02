from pydantic import BaseModel, Field
from datetime import datetime


class BaseUser(BaseModel):
    username: str = Field(..., max_length=15)


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class UserActivity(BaseUser):
    last_login: datetime
    last_request: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

