import json
from functools import wraps
from typing import Callable

import httpx
import redis.asyncio as redis
from fastapi import HTTPException

from app.core.config import settings


# Redis Connection
redis_client = redis.from_url(
    settings.REDIS_URL,
    decode_responses=True
)


# Cache Decorator
def cache(ttl: int = 300):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            key = f"youtube:{func.__name__}:{str(args[1:])}:{str(kwargs)}"

            try:
                cached = await redis_client.get(key)

                if cached:
                    return json.loads(cached)

            except Exception as e:
                print(f"Redis Cache Read Error: {e}")

            result = await func(*args, **kwargs)

            try:
                await redis_client.setex(
                    key,
                    ttl,
                    json.dumps(result)
                )
            except Exception as e:
                print(f"Redis Cache Write Error: {e}")

            return result

        return wrapper

    return decorator


class YouTubeService:

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    # SEARCH VIDEOS
    @cache(ttl=1800)
    async def search_videos(
        self,
        query: str,
        max_results: int = 20
    ):
        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/search",
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": max_results,
                    "key": settings.YOUTUBE_API_KEY,
                },
            )

            if response.status_code != 200:
                print(response.text)
                raise HTTPException(
                    status_code=400,
                    detail="YouTube API Error"
                )

            return response.json()

    # TRENDING VIDEOS
    @cache(ttl=600)
    async def get_trending(
        self,
        region_code: str = "IN",
        max_results: int = 20
    ):
        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/videos",
                params={
                    "part": "snippet,contentDetails,statistics",
                    "chart": "mostPopular",
                    "regionCode": region_code,
                    "maxResults": max_results,
                    "key": settings.YOUTUBE_API_KEY,
                },
            )

            if response.status_code != 200:
                print(response.text)
                raise HTTPException(
                    status_code=400,
                    detail="YouTube API Error"
                )

            return response.json()

    # VIDEO DETAILS
    async def get_video_details(
        self,
        video_id: str
    ):
        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/videos",
                params={
                    "part": "snippet,contentDetails,statistics",
                    "id": video_id,
                    "key": settings.YOUTUBE_API_KEY,
                },
            )

            if response.status_code != 200:
                print(response.text)
                raise HTTPException(
                    status_code=400,
                    detail="YouTube API Error"
                )

            return response.json()

    # RELATED VIDEOS
    @cache(ttl=600)
    async def get_related_videos(
        self,
        video_id: str,
        max_results: int = 20
    ):
        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/search",
                params={
                    "part": "snippet",
                    "relatedToVideoId": video_id,
                    "type": "video",
                    "maxResults": max_results,
                    "key": settings.YOUTUBE_API_KEY,
                },
            )

            if response.status_code != 200:
                print(response.text)
                raise HTTPException(
                    status_code=400,
                    detail="YouTube API Error"
                )

            return response.json()