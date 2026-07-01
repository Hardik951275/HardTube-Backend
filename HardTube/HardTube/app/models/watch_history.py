from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class WatchHistory(Base):
    __tablename__ = "watch_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    video_id = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    thumbnail = Column(String, nullable=True)
    watched_at = Column(DateTime(timezone=True), server_default=func.now())
    watch_duration = Column(Integer, default=0)  # in seconds