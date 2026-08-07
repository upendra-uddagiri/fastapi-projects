from fastapi import FastAPI

from app.database import Base,engine
from app.routers import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="A RESTful API for shortening URLs",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
