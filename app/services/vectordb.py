from typing import List
import numpy as np
from config import get_chroma_client, get_vector_db_collection

# ✅ No type checker complaints now
client = get_chroma_client()
collection = get_vector_db_collection(client)

def store_embeddings(chunks: List[str], embeddings: List[List[float]]) -> None:
    try:
        print(f"📥 Storing {len(chunks)} chunks to ChromaDB...")

        ids = [f"chunk_{i}" for i in range(len(chunks))]
        embedding_array = np.array(embeddings, dtype=np.float32)

        collection.add(
            documents=chunks,
            embeddings=embedding_array,
            ids=ids
        )

        # ✅ Data is automatically persisted with PersistentClient
        # No need to call persist() explicitly
        print(f"✅ Stored {collection.count()} items into collection: {collection.name}")

    except Exception as e:
        raise RuntimeError(f"❌ Failed to store embeddings in ChromaDB: {e}")


def query_similar_chunks(embedding: List[float], n_results: int = 3):
    try:
        return collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
    except Exception as e:
        raise RuntimeError(f"❌ Failed to query ChromaDB: {e}")