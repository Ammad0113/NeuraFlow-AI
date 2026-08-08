from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.routes.auth import get_current_user
from backend.database.models import User, Conversation, ChatMessage
from backend.models.assistant import MessageCreate, ConversationResponse
from backend.services.ai_service import AIService
from typing import List

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])

@router.post("/chat")
def chat(req: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AIService.process_chat(
        db=db,
        user_id=current_user.id,
        conversation_id=req.conversation_id,
        prompt=req.prompt,
        mode=req.mode
    )

@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.updated_at.desc()).all()

@router.get("/conversations/{conv_id}", response_model=ConversationResponse)
def get_conversation(conv_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Conversation).filter(Conversation.id == conv_id, Conversation.user_id == current_user.id).first()
