from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import UserCreate, Token, User, UserActivity
from ..services.auth import AuthService, get_current_user


router = APIRouter(
    prefix='/auth',
)


@router.post('/sign-up', response_model=Token)
def sign_up(
        user_data: UserCreate,
        service: AuthService = Depends()
):
    return service.register_new_user(user_data)


@router.post('/login', response_model=Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.authenticate_user(
        form_data.username,
        form_data.password
    )


@router.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user


@router.get('/activity/{user_id}', response_model=UserActivity)
def get_user_activity(
        user_id: int,
        service: AuthService = Depends()
):
    return service.get_user_activity(user_id=user_id)
