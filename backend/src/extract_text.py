import os
import io
import fitz  # PyMuPDF
import docx
from PIL import Image
import pytesseract
from pdf2image import convert_from_bytes

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF using PyMuPDF (text-based) and fall back to OCR if needed."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text")
    
    # If text is very short, it might be a scanned PDF. Use OCR.
    if len(text.strip()) < 100:
        images = convert_from_bytes(file_bytes)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img, config="--psm 6")
    
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX using python-docx."""
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from images using pytesseract OCR."""
    img = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(img, config="--psm 6")

def get_extracted_text(file_bytes: bytes, filename: str) -> str:
    """Determine file type and extract text."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == ".pdf":
        return extract_text_from_pdf(file_bytes)
    elif ext == ".docx":
        return extract_text_from_docx(file_bytes)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_bytes)
    elif ext == ".txt":
        return file_bytes.decode('utf-8')
    else:
        # Fallback for base64 strings that might just be text
        try:
            return file_bytes.decode('utf-8')
        except:
            raise ValueError(f"Unsupported file format: {ext}")
