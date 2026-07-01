from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)

from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token

router = APIRouter()


# REGISTER
@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):

    # CHECK EMAIL
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    # CHECK USERNAME
    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken",
        )

    # HASH PASSWORD
    hashed_password = hash_password(user.password)

    # CREATE USER
    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# LOGIN
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    # INVALID USER
    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # CREATE TOKEN
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }