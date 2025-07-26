from app.services.chunker import chunk_pdf
from app.services.embedder import embed_chunks
from app.services.vectordb import store_embeddings

file_path = "/home/lotus/pdf_qa/Superman.pdf"  # Make sure it exists
chunks = chunk_pdf(file_path)
embeddings = embed_chunks(chunks)
store_embeddings(chunks, embeddings)
