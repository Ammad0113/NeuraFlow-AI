from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentResponse(BaseModel):
    id: int
    filename: str
    file_type: str
    chunks_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class RAGQuery(BaseModel):
    query: str
    document_ids: Optional[List[int]] = None
    top_k: int = 3

class RAGCitation(BaseModel):
    filename: str
    chunk_index: int
    snippet: str
    score: float

class RAGResponse(BaseModel):
    answer: str
    citations: List[RAGCitation]
