from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ScrapeRequest(BaseModel):
    url: str
    mode: str = "general" # product, news, table, article, generic
    max_items: int = 20

class ScrapeResponse(BaseModel):
    url: str
    title: str
    scraped_count: int
    data: List[Dict[str, Any]]
