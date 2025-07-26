from typing import Any, Dict
from .embedder import embed_chunks
from .vectordb import query_similar_chunks
from config import get_llm_client

llm = get_llm_client()

def ask_question(question: str, n_results: int = 3) -> Dict[str, Any]:
    """
    Full Q&A flow:
    - Embed the question
    - Get similar chunks from ChromaDB
    - Prompt Groq LLM with context
    - Return the answer and metadata
    """
    try:
        # Step 1: Embed the question
        question_embedding = embed_chunks([question])[0]

        # Step 2: Query vector DB
        results = query_similar_chunks(question_embedding, n_results=n_results)

        # Check for None or empty response
        if (
            results is None or
            not isinstance(results, dict) or
            "documents" not in results or
            "distances" not in results or
            not results["documents"] or
            not results["distances"]
        ):
            raise ValueError("No relevant chunks found in the vector database. Try uploading and embedding data first.")

        top_chunks = results["documents"][0]
        similarity_scores = results["distances"][0]

        # Step 3: Create LLM prompt
        context = "\n\n".join(top_chunks)
        prompt = f"""
        You are an expert assistant answering questions based on the provided PDF context.

        Context:
        {context}

        Question:
        {question}

        Instructions:
        - Answer the question using only the information from the context.
        - If the context does not contain enough information, reply: "I don’t know based on the given context."
        - If the question or topic is not present in the provided PDF or its chunks, reply: "The question or topic is not from the PDF you provided."
        - Use clear and simple English in your response.
        - Do not make up information.

        Provide a detailed and accurate answer.
        """

        # Step 4: Call Groq LLM
        response = llm.invoke(prompt)

        # Step 5: Return final structured result
        return {
            "question": question,
            "answer": response.content,
            "retrieved_chunks": top_chunks,
            "similarity_scores": similarity_scores
        }

    except Exception as e:
        raise RuntimeError(f"Failed to answer question: {e}")
