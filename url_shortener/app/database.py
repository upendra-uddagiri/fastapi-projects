from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite database URL
DATABASE_URL = "sqlite:///./url_shortener.db"

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)


# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
