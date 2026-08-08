from pydantic import BaseModel
from typing import List

class PDFAnalysisResponse(BaseModel):
    filename: str
    total_pages: int
    word_count: int
    executive_summary: str
    keywords: List[str]
    identified_risks: List[str]
    sample_text: str
