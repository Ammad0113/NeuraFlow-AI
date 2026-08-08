from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.routes.auth import get_current_user
from backend.database.models import User, DocumentVector
from backend.models.rag import RAGQuery, RAGResponse, DocumentResponse
from backend.services.rag_service import RAGService
from typing import List

router = APIRouter(prefix="/rag", tags=["RAG Knowledge Base"])

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    file_bytes = await file.read()
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file upload.")
    return RAGService.process_and_store_document(db, current_user.id, file_bytes, file.filename)

@router.get("/documents", response_model=List[DocumentResponse])
def list_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(DocumentVector).filter(DocumentVector.user_id == current_user.id).order_by(DocumentVector.created_at.desc()).all()

@router.post("/query", response_model=RAGResponse)
def query_rag(req: RAGQuery, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return RAGService.query_rag(db, current_user.id, req.query, req.document_ids, req.top_k)
