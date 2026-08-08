from fastapi import APIRouter, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.routes.auth import get_current_user
from backend.database.models import User, ReportHistory
from backend.models.reports import ReportGenerateRequest
from backend.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Report Generator"])

@router.post("/generate")
def generate_report(req: ReportGenerateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    content, filename, report_id = ReportService.generate_report(
        db, current_user.id, req.title, req.report_type, req.template, req.custom_notes
    )
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    
    media_type = "application/pdf" if req.report_type.upper() == "PDF" else "text/plain"
    if req.report_type.upper() == "CSV":
        media_type = "text/csv"

    return Response(content=content, media_type=media_type, headers=headers)

@router.get("/history")
def get_report_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(ReportHistory).filter(ReportHistory.user_id == current_user.id).order_by(ReportHistory.created_at.desc()).all()
