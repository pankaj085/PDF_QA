# Dependency to check database connection
from .services.vectordb import collection
from .logging_config import logger


async def get_db_status():
    try:
        if collection is None:
            raise ValueError("Collection is not initialized.")
        count = collection.count()
        return {"connected": True, "count": count}
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return {"connected": False, "count": 0}