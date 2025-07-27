from fastapi import status
from fastapi.responses import JSONResponse
from .logging_config import logger


# Custom exception handler

async def value_error_handler(request, exc):
    logger.error(f"ValueError: {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid input", "detail": str(exc)}
    )

async def runtime_error_handler(request, exc):
    logger.error(f"RuntimeError: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)}
    )