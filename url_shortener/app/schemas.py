from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    short_code: str
    short_url: str


class URLStats(BaseModel):
    original_url: HttpUrl
    short_code: str
    clicks: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
