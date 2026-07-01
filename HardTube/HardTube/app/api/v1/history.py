from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import get_current_user
from app.crud.watch_history import watch_history_crud
from app.models.user import User

router = APIRouter()

@router.post("/add")
async def add_to_history(
    video_id: str,
    title: str,
    thumbnail: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = watch_history_crud.create(
        db=db,
        user_id=current_user.id,
        video_id=video_id,
        title=title,
        thumbnail=thumbnail
    )
    return {"message": "Added to history", "history_id": history.id}

@router.get("/")
async def get_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    history = watch_history_crud.get_user_history(db, current_user.id, limit)
    return history