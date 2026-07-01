from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine

from app.api.v1 import youtube, auth


# CREATE DATABASE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ROUTES
app.include_router(
    youtube.router,
    prefix="/api/v1/youtube",
    tags=["youtube"],
)

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["auth"],
)


@app.get("/")
def root():
    return {"message": "HardTube Backend Running"}