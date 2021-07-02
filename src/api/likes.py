from fastapi import APIRouter, Depends, status, Response
from typing import List

from ..models.likes import Like, LikeCreate
from ..services.likes import LikeService
from ..services.auth import get_current_user
from ..tables import User


router = APIRouter(
    prefix='/like',
)


@router.get('/', response_model=List[Like])
def get_likes(
        user: User = Depends(get_current_user),
        service: LikeService = Depends(),
):
    return service.get_many(user_id=user.id)


@router.post('/', response_model=Like)
def create_like(
        like_data: LikeCreate,
        post_id: int,
        user: User = Depends(get_current_user),
        service: LikeService = Depends(),
):

    return service.create(post_id=post_id, user_id=user.id, like_data=like_data)


@router.delete(
    '/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
def unlike(
    post_id: int,
    user: User = Depends(get_current_user),
    service: LikeService = Depends(),
):
    service.unlike(
        post_id,
        user.id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

