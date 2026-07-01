from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VideoSnippet(BaseModel):
    title: str
    description: Optional[str] = None
    thumbnails: dict
    channelTitle: str
    publishedAt: datetime

class VideoStatistics(BaseModel):
    viewCount: Optional[str] = None
    likeCount: Optional[str] = None

class VideoItem(BaseModel):
    id: str
    snippet: VideoSnippet
    statistics: Optional[VideoStatistics] = None

class YouTubeSearchResponse(BaseModel):
    items: List[dict]
    nextPageToken: Optional[str] = None

class VideoDetailResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    thumbnail: str
    channelTitle: str
    viewCount: Optional[str]
    likeCount: Optional[str]
    publishedAt: datetime