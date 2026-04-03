import os
import uvicorn
import base64
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict

# Import extraction and analysis functions
from extract_text import get_extracted_text
from ai_analysis import analyze_document

app = FastAPI(
    title="Data Extraction API",
    description="AI-Powered Document Analysis & Extraction for GUVI Hackathon",
    version="1.0.0"
)

# API Key Dependency (Compliance with GUVI Tester)
async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    expected_key = os.getenv("API_KEY", "GUVI-AI-2026")
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return x_api_key

# Request Model (Base64 as per spec)
class DocumentRequest(BaseModel):
    fileName: str
    fileType: str  # pdf/docx/image
    fileBase64: str

# Response Model (Aligned with spec)
class EntitiesResponse(BaseModel):
    names: List[str]
    dates: List[str]
    organizations: List[str]
    amounts: List[str]

class DocumentResponse(BaseModel):
    status: str
    fileName: str
    summary: str
    entities: EntitiesResponse
    sentiment: str

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "success", "message": "Data Extraction API is running!"}

@app.post("/api/document-analyze", response_model=DocumentResponse)
async def analyze_document_endpoint(
    request: DocumentRequest,
    api_key: str = Depends(verify_api_key)
):
    """Process Base64 document for AI analysis."""
    try:
        # Decode Base64
        file_bytes = base64.b64decode(request.fileBase64)
        
        # Check size (max 10MB)
        if len(file_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
            
        # Extract text
        extracted_text = get_extracted_text(file_bytes, request.fileName)
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from document")
            
        # AI Analysis
        analysis = analyze_document(extracted_text)
        
        # Format entities to match spec structure
        formatted_entities = {
            "names": [e["text"] for e in analysis["entities"] if e["label"] == "PERSON"],
            "dates": [e["text"] for e in analysis["entities"] if e["label"] == "DATE"],
            "organizations": [e["text"] for e in analysis["entities"] if e["label"] == "ORG"],
            "amounts": analysis["money"]
        }
        
        return {
            "status": "success",
            "fileName": request.fileName,
            "summary": analysis["summary"],
            "entities": formatted_entities,
            "sentiment": analysis["sentiment"].capitalize()
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
