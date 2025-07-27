# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import your custom modules
from .logging_config import logger

from routes.health import router as health_router
from routes.upload_pdf import router as upload_pdf_router
from routes.qa import router as qa_router
from routes.database import router as database_router
from exceptions import value_error_handler, runtime_error_handler




# Initialize FastAPI app
app = FastAPI(
    title="PDF Q&A API",
    description="""
    A sophisticated PDF Question & Answer API that allows you to:
    
    * **Upload PDF files** and automatically chunk and embed them
    * **Ask questions** about your uploaded PDFs using semantic search
    * **Get relevant answers** powered by Groq LLM with context from your documents
    
    The API uses ChromaDB for vector storage and SentenceTransformers for embeddings.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Health",
            "description": "Health check and system status endpoints"
        },
        {
            "name": "Document Management",
            "description": "Upload and manage PDF documents"
        },
        {
            "name": "Question & Answer",
            "description": "Ask questions about your uploaded documents"
        },
        {
            "name": "Database",
            "description": "Database statistics and management"
        }
    ]
)

app.include_router(health_router)
app.include_router(upload_pdf_router)
app.include_router(qa_router)
app.include_router(database_router)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RuntimeError, runtime_error_handler)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Lifespan event handler (replaces deprecated on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for startup and shutdown events."""
    logger.info("Starting PDF Q&A API...")
    logger.info("Application startup complete")
    yield
    logger.info("Shutting down PDF Q&A API...")

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )