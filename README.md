# Data Extraction API

## Description
This project is an intelligent document processing system built for the GUVI Hackathon. It automatically extracts, analyzes, and summarizes content from various document formats including PDF, DOCX, and images. The system uses a hybrid approach of traditional text extraction (PyMuPDF), OCR (Tesseract), and state-of-the-art AI models for high-quality data analysis.

## Tech Stack
- **Language**: Python 3.13 (Backend), JavaScript/React (Frontend)
- **Frameworks**: FastAPI, Vite, Tailwind CSS
- **AI Models**: 
  - spaCy (`en_core_web_sm`) for Named Entity Recognition
  - BART (`facebook/bart-large-cnn`) for Summarization
  - DistilBERT for Sentiment Analysis
- **Key Libraries**: PyMuPDF (fitz), python-docx, pytesseract, transformers, torch

## Setup Instructions
1. **Clone the repository**:
   ```bash
   git clone <your-repo-link>
   cd DocuAI-Extractor
   ```
2. **Install dependencies**:
   ```bash
   cd backend/src
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
3. **Set environment variables**:
   Create a `.env` file in `backend/src` based on `.env.example`:
   ```env
   API_KEY=your_secret_api_key
   PORT=8000
   ```
4. **Run the application**:
   ```bash
   uvicorn main:app --reload
   ```

## Approach
Our data extraction strategy follows a robust multi-stage pipeline:
- **Text Extraction**: We prioritize native text extraction using PyMuPDF and python-docx. For scanned documents or images, we fall back to Tesseract OCR with Layout Preservation (PSM 6).
- **Summarization**: We use the BART large-cnn model to generate concise, abstractive summaries of the extracted text.
- **Entity Extraction**: We utilize spaCy's pre-trained English models to identify names, organizations, and dates. Monetary amounts are extracted using specialized regex patterns to ensure precision across various currency symbols.
- **Sentiment Analysis**: A DistilBERT model fine-tuned on SST-2 provides accurate Positive/Neutral/Negative classification.

## AI Tools Used (Mandatory Disclosure)
- **Trae IDE**: Used for project structure generation, logic implementation, and debugging.
- **Claude 3.5 Sonnet (via Trae)**: Assisted in building the FastAPI backend, React dashboard, and AI model integration logic.
- **GitHub Copilot**: Used for boilerplate code and documentation assistance.

### Prerequisites
- Python 3.9+
- Node.js 18+
- Tesseract OCR installed on your system.
- Poppler installed on your system (for PDF to image conversion).

### Running the Backend
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows)
4. `pip install -r requirements.txt`
5. `python -m spacy download en_core_web_sm`
6. `uvicorn main:app --reload`

### Running the Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## API Documentation
The API is self-documented with Swagger. Visit `http://localhost:8000/docs` when the backend is running.

- **GET /**: Health check endpoint.
- **POST /api/document-analyze**: Analyze a document (base64 payload).
  - Request body: JSON with `fileName`, `fileType`, `fileBase64`.
  - Headers: `X-API-Key: <api-key>`
  - Response: JSON with `status`, `fileName`, `summary`, `entities`, `sentiment`.

### GUI Endpoint Tester (GUVI compliance)
In the frontend app, you can now enter any deployed endpoint URL and API key in the top tester pane, then click **Test Endpoint**. It sends a sample payload (text) to verify authentication, payload handling, and response format.

## Screenshots
(Add screenshots of the dashboard and upload zone here)
