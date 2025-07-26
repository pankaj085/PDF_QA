# Pydantic models for request/response validation
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="The question to ask about the PDF")
    n_results: Optional[int] = Field(2, ge=1, le=10, description="Number of similar chunks to retrieve")

    @field_validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty or just whitespace')
        return v.strip()

class QuestionResponse(BaseModel):
    question: str
    answer: str
    retrieved_chunks: List[str]
    similarity_scores: List[float]
    timestamp: datetime
    processing_time_ms: float

class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int
    text_length: int
    timestamp: datetime
    processing_time_ms: float

class DatabaseStats(BaseModel):
    collection_name: str
    total_chunks: int
    database_path: str
    embedding_model: str

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database_connected: bool
    total_chunks: int