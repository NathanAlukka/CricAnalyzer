from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import get_settings
from app.db.session import init_db

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend API for the CricAnalyzer auction assistant.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables automatically in development when configured."""

    if settings.auto_create_tables:
        init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "CricAnalyzer API is running.",
        "docs": "/docs",
        "health": "/api/health",
    }
