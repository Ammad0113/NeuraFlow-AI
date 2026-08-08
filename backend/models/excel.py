from pydantic import BaseModel
from typing import Dict, Any, List

class ExcelCleanOptions(BaseModel):
    remove_duplicates: bool = True
    fill_missing_numeric: str = "mean" # mean, median, zero
    fill_missing_text: str = "Unknown"

class ExcelSummaryResponse(BaseModel):
    rows: int
    columns: int
    column_names: List[str]
    missing_values: Dict[str, int]
    duplicates_count: int
    summary_stats: Dict[str, Any]
    ai_insights: List[str]
