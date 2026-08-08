from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from backend.routes.auth import get_current_user
from backend.database.models import User
from backend.models.pdf import PDFAnalysisResponse
from backend.services.pdf_service import PDFService

router = APIRouter(prefix="/pdf", tags=["PDF Intelligence"])

@router.post("/analyze", response_model=PDFAnalysisResponse)
async def analyze_pdf(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Must upload a valid PDF document.")
    file_bytes = await file.read()
    return PDFService.analyze_pdf(file_bytes, file.filename)
