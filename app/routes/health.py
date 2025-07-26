from fastapi import APIRouter, Depends
from datetime import datetime

from models import HealthResponse
from dependencies import get_db_status
from models import HealthResponse


router = APIRouter(
    prefix="",
    tags=["Health"]
)


@router.get("/", tags=["Health"], summary="Welcome endpoint with API information")
async def root():
    """Welcome endpoint with API information."""
    return {
        "message": "Welcome to PDF Q&A API",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(db_status: dict = Depends(get_db_status)):
    """Comprehensive health check endpoint."""
    return HealthResponse(
        status="healthy" if db_status["connected"] else "unhealthy",
        timestamp=datetime.now(),
        database_connected=db_status["connected"],
        total_chunks=db_status["count"]
    )