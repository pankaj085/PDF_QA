# app/config.py

import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from chromadb import PersistentClient
from chromadb.api import ClientAPI


# Load environment variables from .env file
load_dotenv()

# Config values
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3-8b-8192")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "pdf_chunks")


def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_llm_client(model: str = LLM_MODEL_NAME) -> ChatGroq:
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY in .env")
    return ChatGroq(model=model)


def get_chroma_client() -> ClientAPI:
    """
    Returns a persistent ChromaDB client instance.
    """
    return PersistentClient(path=CHROMA_DB_PATH)


def get_vector_db_collection(client: ClientAPI):
    """
    Returns or creates a collection in ChromaDB.
    """
    return client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
