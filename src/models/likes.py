from pydantic import BaseModel
from datetime import date


class BaseLike(BaseModel):
    date: date

    class Config:
        orm_mode = True


class Like(BaseLike):
    id: int
    user_id: int
    post_id: int


class LikeCreate(BaseLike):
    pass
