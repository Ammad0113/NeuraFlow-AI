from .session import Base, engine, get_db, SessionLocal
from .models import User, Conversation, ChatMessage, DocumentVector, MLModelArtifact, AutomationLog, ReportHistory

def init_db():
    Base.metadata.create_all(bind=engine)
