import random
import string

from sqlalchemy.orm import Session

from app.models import URL

def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits

    return "".join(random.choice(characters) for _ in range(length))


def create_unique_short_code(db: Session) -> str:
    while True:
        code = generate_short_code()

        existing = db.query(URL).filter(URL.short_code == code).first()

        if not existing:
            return code
