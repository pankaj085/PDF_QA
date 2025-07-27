from fastapi import APIRouter, HTTPException, status
from ..models import DatabaseStats
from ..services.vectordb import collection
from ..logging_config import logger


router = APIRouter(
    prefix="",
    tags=["Database"]
)


@router.get("/database/stats", response_model=DatabaseStats, tags=["Database"])
async def get_database_stats():
    """Get statistics about the vector database."""
    try:
        from ..config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME, EMBEDDING_MODEL_NAME
        
        return DatabaseStats(
            collection_name=CHROMA_COLLECTION_NAME,
            total_chunks=collection.count(),
            database_path=CHROMA_DB_PATH,
            embedding_model=EMBEDDING_MODEL_NAME
        )
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve database statistics"
        )

@router.delete("/database/clear", tags=["Database"])
async def clear_database():
    """Clear all documents from the vector database."""
    try:
        # Get all IDs and delete them
        result = collection.get()
        if result and result.get('ids'):
            collection.delete(ids=result['ids'])
            deleted_count = len(result['ids'])
            logger.info(f"Cleared {deleted_count} chunks from database")
            return {"message": f"Successfully cleared {deleted_count} chunks from database"}
        else:
            return {"message": "Database was already empty"}
            
    except Exception as e:
        logger.error(f"Failed to clear database: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear database"
        )