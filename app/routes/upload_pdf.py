import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from datetime import datetime

from logging_config import logger
from models import UploadResponse
from services.chunker import chunk_pdf, extract_text_from_pdf
from services.embedder import embed_chunks
from services.vectordb import store_embeddings
from services.vectordb import collection


router = APIRouter(
    prefix="",
    tags=["Document Management"]
)


@router.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file.
    
    This endpoint:
    1. Validates the uploaded file is a PDF
    2. Extracts text from the PDF
    3. Chunks the text into manageable pieces
    4. Creates embeddings for each chunk
    5. Stores everything in the vector database
    """
    start_time = datetime.now()
    temp_file_path = None  # Initialize here to ensure it's always defined
    
    # Validate file type
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    if file.size is None or file.size > 50 * 1024 * 1024:  # 50MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds 50MB limit"
        )
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        logger.info(f"Processing PDF: {file.filename or 'unknown'}")
        
        # Clear previous chunks from the vector database
        existing = collection.get()
        if existing and existing.get('ids'):
            collection.delete(ids=existing['ids'])
            logger.info(f"Cleared {len(existing['ids'])} previous chunks from database")
        
        # Extract text and validate
        full_text = extract_text_from_pdf(temp_file_path)
        if not full_text.strip():
            raise ValueError("PDF appears to be empty or contains no extractable text")
        
        # Chunk the PDF
        chunks = chunk_pdf(temp_file_path)
        if not chunks:
            raise ValueError("Failed to create chunks from PDF")
        
        logger.info(f"Created {len(chunks)} chunks from {file.filename or 'unknown'}")
        
        # Create embeddings
        embeddings = embed_chunks(chunks)
        
        # Store in vector database
        store_embeddings(chunks, embeddings)
        
        # Clean up temporary file
        if temp_file_path:
            os.unlink(temp_file_path)
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        logger.info(f"Successfully processed {file.filename or 'unknown'} in {processing_time:.2f}ms")
        
        return UploadResponse(
            message="PDF uploaded and processed successfully",
            filename=file.filename if file.filename else "unknown.pdf",
            chunks_created=len(chunks),
            text_length=len(full_text),
            timestamp=datetime.now(),
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        # Clean up temporary file on error
        if temp_file_path:
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        logger.error(f"Failed to process PDF {file.filename or 'unknown'}: {e}")
        
        if isinstance(e, (ValueError, RuntimeError)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process PDF file"
            )