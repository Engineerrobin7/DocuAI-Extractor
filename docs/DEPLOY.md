# Deployment Guide: DocuAI-Extractor

## Backend (Render.com)
1. **Create a new Web Service** on Render.
2. **Connect your GitHub repository**.
3. **Configure the service**:
   - **Runtime**: Python
   - **Build Command**: `pip install -r backend/requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   - `PORT`: 8000
   - `API_KEY`: Set your secret key (e.g., `GUVI-AI-2026`).
5. **Important**: Tesseract and Poppler are required for OCR and PDF processing. On Render, you may need to use a Custom Dockerfile or use a buildpack that includes these system dependencies.

## Frontend (Render Static or Vercel)
### Render Static Site
1. **Create a new Static Site**.
2. **Configure the service**:
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
3. **Environment Variables**:
   - `VITE_API_URL`: Your backend URL (e.g., `https://docuai-backend.onrender.com`)
   - `VITE_API_KEY`: The same key as set in your backend.

### Vercel (Alternative)
1. **Push your code to GitHub**.
2. **Import the project** in Vercel.
3. **Override the root directory** to `frontend`.
4. **Add environment variables**: `VITE_API_URL` and `VITE_API_KEY`.

## Testing with CURL
```bash
curl -X 'POST' \
  'http://localhost:8000/process' \
  -H 'accept: application/json' \
  -H 'X-API-Key: GUVI-AI-2026' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_test_file.pdf;type=application/pdf'
```
