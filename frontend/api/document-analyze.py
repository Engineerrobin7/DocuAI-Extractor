import os
import sys
import json
import base64
from pathlib import Path

# Add backend src path so we can reuse extraction/analysis logic in this monorepo API function
ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / ".." / "backend" / "src"
sys.path.append(str(BACKEND_SRC))

from extract_text import get_extracted_text
from ai_analysis import analyze_document

DEFAULT_API_KEY = os.getenv("API_KEY", "GUVI-AI-2026")


def _json_response(status_code, data):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(data)
    }


def handler(request):
    try:
        api_key = request.headers.get("x-api-key") or request.headers.get("X-API-Key")
        if api_key != DEFAULT_API_KEY:
            return _json_response(401, {"detail": "Invalid or missing API key"})

        body = request.json() if hasattr(request, "json") else json.loads(request.body.decode("utf-8"))

        file_name = body.get("fileName")
        file_type = body.get("fileType")
        file_base64 = body.get("fileBase64")

        if not file_name or not file_type or not file_base64:
            return _json_response(400, {"detail": "fileName, fileType, fileBase64 are required"})

        file_bytes = base64.b64decode(file_base64)

        if len(file_bytes) > 10 * 1024 * 1024:
            return _json_response(413, {"detail": "File too large (max 10MB)"})

        extracted_text = get_extracted_text(file_bytes, file_name)
        if not extracted_text.strip():
            return _json_response(400, {"detail": "No text extracted from document"})

        analysis = analyze_document(extracted_text)

        formatted_entities = {
            "names": [e["text"] for e in analysis.get("entities", []) if e.get("label") == "PERSON"],
            "dates": [e["text"] for e in analysis.get("entities", []) if e.get("label") == "DATE"],
            "organizations": [e["text"] for e in analysis.get("entities", []) if e.get("label") == "ORG"],
            "amounts": analysis.get("money", [])
        }

        return _json_response(200, {
            "status": "success",
            "fileName": file_name,
            "summary": analysis.get("summary", ""),
            "entities": formatted_entities,
            "sentiment": analysis.get("sentiment", "NEUTRAL").upper()
        })

    except Exception as err:
        return _json_response(500, {"detail": str(err)})
