from fastapi import APIRouter, Depends

from ..models.posts import Post, PostCreate
from ..services.posts import PostService
from ..services.auth import get_current_user
from ..tables import User


router = APIRouter(
    prefix='/post',
)


@router.get('/{post_id}', response_model=Post)
def get_post(
        post_id: int,
        user: User = Depends(get_current_user),
        service: PostService = Depends(),
):
    return service.get(post_id=post_id, user_id=user.id)


@router.post('/', response_model=Post)
def create_post(
        post_data: PostCreate,
        user: User = Depends(get_current_user),
        service: PostService = Depends(),
):

    return service.create(post_data=post_data, user_id=user.id)
