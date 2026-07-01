from sqlalchemy.orm import Session
from app.models.watch_history import WatchHistory
from typing import List

class WatchHistoryCRUD:
    def create(self, db: Session, user_id: int, video_id: str, title: str, thumbnail: str = None):
        history = WatchHistory(
            user_id=user_id,
            video_id=video_id,
            title=title,
            thumbnail=thumbnail
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history

    def get_user_history(self, db: Session, user_id: int, limit: int = 20) -> List[WatchHistory]:
        return db.query(WatchHistory)\
            .filter(WatchHistory.user_id == user_id)\
            .order_by(WatchHistory.watched_at.desc())\
            .limit(limit)\
            .all()

watch_history_crud = WatchHistoryCRUD()