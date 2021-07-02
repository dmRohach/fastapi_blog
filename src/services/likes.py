from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from typing import List, Optional

from .. import tables
from ..database import get_session, Session
from ..models.likes import LikeCreate
from .posts import PostService


class LikeService:
    def __init__(
            self,
            post_service: PostService = Depends(),
            session: Session = Depends(get_session)
    ):
        self.post_service = post_service
        self.session = session

    def create(self, post_id: int, user_id: int, like_data: LikeCreate) -> tables.Like:
        exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Post already liked',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        like = tables.Like(
            **like_data.dict(),
            post_id=post_id,
            user_id=user_id
        )

        if not self._get(post_id, user_id):
            self.session.add(like)
            self.session.commit()
            return like
        else:
            raise exception

    def unlike(self, post_id: int, user_id: int):
        exception = HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Post is not liked',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        like = self._get(post_id, user_id)

        if like:
            self.session.delete(like)
            self.session.commit()
        else:
            raise exception

    def get_many(self, user_id: int) -> List[tables.Like]:
        likes = (
            self.session
            .query(tables.Like)
            .filter(tables.Like.user_id == user_id)
            .order_by(
                tables.Like.date.desc(),
                tables.Like.id.desc(),
            )
            .all()
        )
        return likes

    def _get(self, post_id: int, user_id: int) -> Optional[tables.Like]:
        self.post_service.get(post_id=post_id, user_id=user_id)
        if self.post_service:
            like = (
                self.session
                .query(tables.Like)
                .filter(
                    tables.Like.user_id == user_id,
                    tables.Like.post_id == post_id,
                )
                .first()
            )

            return like
