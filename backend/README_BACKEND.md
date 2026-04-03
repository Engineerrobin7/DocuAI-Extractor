# DocuAI-Extractor Backend

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Install spaCy model: `python -m spacy download en_core_web_sm`
5. Run: `uvicorn main:app --reload`

## API Endpoints
- `POST /process`: Upload PDF/DOCX/Images for AI analysis.
- `GET /`: Health check.

## Features
- OCR with Tesseract
- Text extraction with PyMuPDF and python-docx
- NER with spaCy
- Summarization with BART
- Sentiment analysis with DistilBERT
