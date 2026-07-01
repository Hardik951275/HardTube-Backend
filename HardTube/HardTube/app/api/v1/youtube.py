from fastapi import APIRouter
from app.services.youtube_service import YouTubeService

router = APIRouter()

youtube_service = YouTubeService()


@router.get("/trending")
async def get_trending(
    region: str = "IN",
    max_results: int = 20
):
    return await youtube_service.get_trending(
        region,
        max_results
    )


@router.get("/search")
async def search(
    q: str,
    max_results: int = 20
):
    return await youtube_service.search_videos(
        q,
        max_results
    )


@router.get("/video/{video_id}")
async def video_details(
    video_id: str
):
    return await youtube_service.get_video_details(
        video_id
    )


@router.get("/related/{video_id}")
async def related_videos(
    video_id: str,
    max_results: int = 20
):
    return await youtube_service.get_related_videos(
        video_id,
        max_results
    )