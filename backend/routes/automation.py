from fastapi import APIRouter, Depends, UploadFile, File, Response, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.routes.auth import get_current_user
from backend.database.models import User, AutomationLog
from backend.models.automation import FolderOrganizeRequest, FileRenameRequest
from backend.services.automation_service import AutomationService
from typing import List

router = APIRouter(prefix="/automation", tags=["Python Automation Center"])

@router.post("/organize-folder")
def organize_folder(req: FolderOrganizeRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AutomationService.organize_folder(db, current_user.id, req.directory_path)

@router.post("/batch-rename")
def batch_rename(req: FileRenameRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AutomationService.batch_rename(db, current_user.id, req.directory_path, req.prefix, req.extension_filter)

@router.post("/pdf-merge")
async def pdf_merge(files: List[UploadFile] = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bytes_list = []
    filenames = []
    for f in files:
        bytes_list.append(await f.read())
        filenames.append(f.filename)
    
    merged_bytes, out_name = AutomationService.merge_pdfs(db, current_user.id, bytes_list, filenames)
    headers = {"Content-Disposition": f"attachment; filename={out_name}"}
    return Response(content=merged_bytes, media_type="application/pdf", headers=headers)

@router.get("/history")
def get_automation_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(AutomationLog).filter(AutomationLog.user_id == current_user.id).order_by(AutomationLog.created_at.desc()).all()
