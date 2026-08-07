from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import URLCreate, URLResponse, URLStats
from app.crud import (
    create_short_url,
    get_url_by_code,
    increment_clicks,
    get_url_stats,
)
router = APIRouter()


@router.get("/")
def home():
    return {"message": "URL Shortener API is Running"}


@router.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLCreate, db: Session = Depends(get_db)):
    url = create_short_url(db, request)

    return URLResponse(
        short_code=url.short_code,
        short_url=f"http://localhost:8000/{url.short_code}",
    )


@router.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    url = get_url_by_code(db, short_code)

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    increment_clicks(db, url)
    print(url.original_url)
    return RedirectResponse(url=url.original_url)


@router.get("/stats/{short_code}", response_model=URLStats)
def url_stats(short_code: str, db: Session = Depends(get_db)):
    url = get_url_stats(db, short_code)

    if not url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found",
        )

    return url
