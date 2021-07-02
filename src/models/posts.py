from pydantic import BaseModel
from typing import List

from .likes import Like


class BasePost(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class Post(BasePost):
    id: int
    likes: List[Like]


class PostCreate(BasePost):
    pass
