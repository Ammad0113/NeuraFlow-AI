from pydantic import BaseModel
from typing import Optional, Dict, Any

class ReportGenerateRequest(BaseModel):
    title: str
    report_type: str # PDF, Markdown, CSV
    template: str # executive, technical, financial, analytics
    data_source: Optional[str] = None
    custom_notes: Optional[str] = None

class ReportResponse(BaseModel):
    report_id: int
    title: str
    report_type: str
    download_url: str
