from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from models import QuestionRequest, QuestionResponse
from services.query import ask_question
from dependencies import get_db_status
from logging_config import logger


router = APIRouter(
    prefix="",
    tags=["Question & Answer"]
)


@router.post("/ask", response_model=QuestionResponse, tags=["Question & Answer"])
async def ask_question_endpoint(request: QuestionRequest, db_status: dict = Depends(get_db_status)):
    """
    Ask a question about your uploaded PDF documents.
    
    This endpoint:
    1. Validates that documents exist in the database
    2. Embeds your question
    3. Finds the most similar document chunks
    4. Uses Groq LLM to generate an answer based on the context
    """
    start_time = datetime.now()
    
    # Check if database has documents
    if not db_status["connected"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vector database is not available"
        )
    
    if db_status["count"] == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No documents found in database. Please upload a PDF first."
        )
    
    try:
        logger.info(f"Processing question: {request.question}")
        
        # Ask the question
        result = ask_question(request.question, n_results=request.n_results or 2)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        logger.info(f"Question answered in {processing_time:.2f}ms")
        
        return QuestionResponse(
            question=result["question"],
            answer=result["answer"],
            retrieved_chunks=result["retrieved_chunks"],
            similarity_scores=result["similarity_scores"],
            timestamp=datetime.now(),
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Failed to answer question: {e}")
        
        if isinstance(e, (ValueError, RuntimeError)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process question"
            )