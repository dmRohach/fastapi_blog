from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from ..database import get_session
from .. import tables


class AnalyticService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def daily_analytics(self, date_from: date, date_to: date, user_id: int) -> dict:
        likes = (
                self.session
                .query(tables.Like.date, func.count(tables.Like.id))
                .filter(
                    tables.Like.user_id == user_id,
                    tables.Like.date >= date_from,
                    tables.Like.date <= date_to
                )
                .group_by(tables.Like.date)
                .all())
        print(likes)

        return {Date: count for Date, count in likes}
