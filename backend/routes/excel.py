from fastapi import APIRouter, Depends, UploadFile, File, Form, Response, HTTPException
from backend.routes.auth import get_current_user
from backend.database.models import User
from backend.services.excel_service import ExcelService

router = APIRouter(prefix="/excel", tags=["Excel Intelligence"])

@router.post("/inspect")
async def inspect_excel(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    file_bytes = await file.read()
    return ExcelService.inspect_dataset(file_bytes, file.filename)

@router.post("/clean")
async def clean_excel(
    file: UploadFile = File(...),
    remove_duplicates: bool = Form(True),
    fill_missing_numeric: str = Form("mean"),
    fill_missing_text: str = Form("Unknown"),
    current_user: User = Depends(get_current_user)
):
    file_bytes = await file.read()
    cleaned_bytes, filename = ExcelService.clean_dataset(
        file_bytes, file.filename, remove_duplicates, fill_missing_numeric, fill_missing_text
    )
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(content=cleaned_bytes, media_type="application/octet-stream", headers=headers)
