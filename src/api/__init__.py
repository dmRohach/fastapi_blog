from fastapi import APIRouter
from .posts import router as posts_router
from .auth import router as users_router
from .likes import router as likes_router
from .analytics import router as analytics_router


router = APIRouter()
router.include_router(users_router)
router.include_router(posts_router)
router.include_router(likes_router)
router.include_router(analytics_router)
