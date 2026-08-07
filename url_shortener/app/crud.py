from sqlalchemy.orm import Session

from app.models import URL
from app.schemas import URLCreate
from app.utils import create_unique_short_code

def create_short_url(db: Session, request: URLCreate):
    short_code = create_unique_short_code(db)

    new_url = URL(
        original_url=str(request.original_url),
        short_code=short_code,
        clicks=0,
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return new_url


def get_url_by_code(db: Session, short_code: str):
    return db.query(URL).filter(URL.short_code == short_code).first()


def increment_clicks(db: Session, url: URL):
    url.clicks += 1
    db.commit()
    db.refresh(url)

    return url


def get_url_stats(db: Session, short_code: str):
    return db.query(URL).filter(URL.short_code == short_code).first()
