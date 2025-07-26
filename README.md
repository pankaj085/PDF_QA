# PDF Q&A API

A modular FastAPI backend for semantic question answering over PDF documents.  
Upload a PDF, ask questions, and get context-aware answers powered by Groq LLM, SentenceTransformers, and ChromaDB.

---

## Features

- **Upload PDF files**: Automatically chunk and embed your documents for semantic search.
- **Ask questions**: Get answers grounded in your PDF content using Groq LLM.
- **Semantic search**: Retrieve relevant text chunks using vector similarity.
- **Database management**: View stats, clear stored chunks, and monitor health.
- **Modular codebase**: Organized with routers, services, models, and dependencies for maintainability.

---

## Tech Stack

- **FastAPI**: Web framework for building APIs.
- **SentenceTransformers**: Generates text embeddings for semantic search.
- **ChromaDB**: Vector database for storing and querying document chunks.
- **Groq LLM**: Large language model for answering questions.
- **Pydantic**: Data validation and serialization.
- **Uvicorn**: ASGI server for running FastAPI.

---

## API Keys & Secrets

This app requires several secrets and configuration values, which must be set in a `.env` file in the project root:

- `GROQ_API_KEY`: Your Groq LLM API key (required for question answering).
- `LLM_MODEL_NAME`: The name of the Groq LLM model to use (default: `llama3-8b-8192`).
- `EMBEDDING_MODEL_NAME`: The name of the SentenceTransformers embedding model (default: `all-MiniLM-L6-v2`).
- `CHROMA_DB_PATH`: Path to ChromaDB persistent storage (default: `./chroma_db`).
- `CHROMA_COLLECTION_NAME`: Name of the ChromaDB collection for storing PDF chunks (default: `pdf_chunks`).

**Important:**  
Never commit your `.env` file or secrets to public repositories.

---

## Logging

- All API activity and errors are logged to `pdf_qa_app.log` in the `app/` directory.
- This log file is automatically created and updated when the server runs.
- You can review this file for debugging, monitoring, and auditing purposes.

---

## Quick Start

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/pdf-qa.git
    cd pdf-qa
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**
    - Copy this `.env.example` to `.env` and fill in your secrets (Groq API key, etc).
    ```
    # Groq API key for LLM access
    GROQ_API_KEY=

    # Name of the LLM model to use
    LLM_MODEL_NAME=

    # Name of the embedding model to use (note: spelling should be EMBEDDING_MODEL_NAME)
    EMEDDING_MODEL_NAME=

    # Path to ChromaDB persistent storage
    CHROMA_DB_PATH=

    # Name of the ChromaDB collection for storing PDF chunks
    CHROMA_COLLECTION_NAME=
    ```

5. **Run the app**
    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the API documentation**
    - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

---

## API Endpoints

- `POST /upload-pdf` — Upload and process a PDF file.
- `POST /ask` — Ask a question about your uploaded PDF.
- `GET /health` — Health check endpoint.
- `GET /database/stats` — Get vector database statistics.
- `DELETE /database/clear` — Clear all stored chunks.

---

## Project Structure

```
app/
  main.py
  models.py
  config.py
  dependencies.py
  exceptions.py
  routes/
    health.py
    upload_pdf.py
    qa.py
    database.py
  services/
    chunker.py
    embedder.py
    vectordb.py
    query.py
.env
requirements.txt
README.md
LICENSE
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributing

Pull requests and issues are welcome!  
Please open an issue for bugs or feature requests, and submit pull requests for review.