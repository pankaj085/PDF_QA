# app/embedder.py

from typing import List
import numpy as np
from config import get_embedding_model

# Load the embedding model (SentenceTransformer instance)
embedding_model = get_embedding_model()

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Embeds a list of text chunks using the configured SentenceTransformer model.
    
    Args:
        chunks: List of text strings (chunks).

    Returns:
        List of vector embeddings (each embedding is a list of floats).
    """
    try:
        embeddings = embedding_model.encode(chunks)
        return embeddings.tolist()  # Convert from numpy array to list of lists
    except Exception as e:
        raise RuntimeError(f"Error during embedding: {e}")
