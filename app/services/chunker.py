# app/chunker.py

from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts and cleans all text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        A single string containing the full cleaned text of the PDF.
    """
    try:
        reader = PdfReader(pdf_path)
        all_text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                clean_text = ' '.join(page_text.split())  # Remove excess whitespace
                all_text += clean_text + "\n\n"

        return all_text.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")

def chunk_pdf(pdf_path: str, chunk_size: int = 1000, chunk_overlap: int = 150) -> List[str]:
    """
    Full pipeline: Load a PDF file and split it into clean chunks.

    Args:
        pdf_path: Path to the PDF file.
        chunk_size: Max size of each chunk.
        chunk_overlap: Overlap between chunks.

    Returns:
        A list of string chunks from the PDF.
    """
    full_text = extract_text_from_pdf(pdf_path)
    return chunk_text(full_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 150) -> List[str]:
    """
    Splits long text into overlapping chunks using RecursiveCharacterTextSplitter.

    Args:
        text: Full cleaned text.
        chunk_size: Maximum characters in one chunk.
        chunk_overlap: Number of overlapping characters between chunks.

    Returns:
        A list of text chunks.
    """
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_text(text)
        return chunks

    except Exception as e:
        raise RuntimeError(f"Error while chunking text: {e}")
