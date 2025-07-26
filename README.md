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
    - Copy `.env.example` to `.env` and fill in your secrets (Groq API key, etc).

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