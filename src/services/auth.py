from passlib.hash import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from .. import tables
from ..models.auth import User, Token, UserCreate, UserActivity
from ..config import settings
from ..database import get_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')   #Reading and checking token (redirect to login if token is not provided


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


def update_logs(
        user_id: int,
):
    session = next(get_session())
    user = (
        session
        .query(tables.User)
        .filter(tables.User.id == user_id)
        .first()
    )
    user.last_request = datetime.utcnow()
    session.commit()


class AuthService:
    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            print(
                token)
            print(settings.jwt_secret)
            print(settings.jwt_algorithm)
            raise exception

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
            update_logs(user_id=user.id)

        except ValueError:
            raise exception from None

        return user

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)

        now = datetime.utcnow()

        payload = {     # Token's data
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expiration),    # token lifetime
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm
        )
        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:
        user = tables.User(
            username=user_data.username,
            password_hash=self.hash_password(user_data.password)
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect username or password',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )

        user = (
            self.session
            .query(tables.User)
            .filter(tables.User.username == username)
            .first()
        )

        if not user:    # If input username is not in base
            raise exception

        if not self.verify_password(password, user.password_hash):      # If input password is incorrect
            raise exception

        user.last_login = datetime.utcnow()
        self.session.commit()
        return self.create_token(user)

    def get_user_activity(self, user_id: int) -> UserActivity:
        user = (
            self.session
            .query(tables.User)
            .filter(tables.User.id == user_id)
            .first()
        )
        return user




