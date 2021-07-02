from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from typing import Optional

from .. import tables
from ..database import get_session
from ..models.posts import PostCreate


class PostService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create(self, user_id: int, post_data: PostCreate) -> tables.Post:
        post = tables.Post(
            **post_data.dict(),
            user_id=user_id
        )
        self.session.add(post)
        self.session.commit()
        return post

    def get(self, post_id: int, user_id: int) -> tables.Post:
        post = self._get(post_id, user_id)
        return post

    def _get(self, post_id: int, user_id: int) -> Optional[tables.Post]:
        post = (
            self.session
            .query(tables.Post)
            .filter(
                tables.Post.user_id == user_id,
                tables.Post.id == post_id,
            )
            .first()
        )
        if not post:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return post

