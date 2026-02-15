import io
import PyPDF2
from docx import Document
from typing import Optional, Tuple
import streamlit as st

MAX_FILE_SIZE_MB = 20

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(docx_file) -> str:
    """Extract text from DOCX file."""
    try:
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {str(e)}")


def extract_text_from_txt(txt_file) -> str:
    """Extract text from TXT file."""
    try:
        text = txt_file.read().decode('utf-8')
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from TXT: {str(e)}")


def process_uploaded_file(uploaded_file_or_path) -> tuple[str, str]:
    """Process uploaded file or path and extract text content."""
    import os
    
    if isinstance(uploaded_file_or_path, str):
        file_path = uploaded_file_or_path
        file_name = os.path.basename(file_path)
    else:
        file_path = None
        file_name = uploaded_file_or_path.name

    file_name_no_ext = os.path.splitext(file_name)[0]
    file_extension = file_name.lower().split('.')[-1]

    if file_extension == 'pdf':
        text_content = extract_text_from_pdf(uploaded_file_or_path if file_path is None else open(file_path, "rb"))
    elif file_extension == 'docx':
        text_content = extract_text_from_docx(uploaded_file_or_path if file_path is None else file_path)
    elif file_extension == 'txt':
        text_content = extract_text_from_txt(uploaded_file_or_path if file_path is None else file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Please upload PDF, DOCX, or TXT files.")

    if not text_content.strip():
        raise ValueError("No text content found in the uploaded file.")

    return file_name_no_ext, text_content
