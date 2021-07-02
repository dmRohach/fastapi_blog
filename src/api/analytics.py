from fastapi import APIRouter, Depends
from datetime import date

from ..tables import User
from ..services.auth import get_current_user
from ..services.analytics import AnalyticService


router = APIRouter(
    prefix='/api',
)


@router.get('/analytics', response_model=dict)
def analytics(
        date_from: date,
        date_to: date,
        user: User = Depends(get_current_user),
        service: AnalyticService = Depends(),
):
    return service.daily_analytics(
        date_from=date_from,
        date_to=date_to,
        user_id=user.id
    )