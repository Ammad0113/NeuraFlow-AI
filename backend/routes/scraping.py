from fastapi import APIRouter, Depends, Response
from backend.routes.auth import get_current_user
from backend.database.models import User
from backend.models.scraping import ScrapeRequest, ScrapeResponse
from backend.services.scraping_service import ScrapingService

router = APIRouter(prefix="/scraping", tags=["Web Scraping Studio"])

@router.post("/scrape", response_model=ScrapeResponse)
def scrape(req: ScrapeRequest, current_user: User = Depends(get_current_user)):
    return ScrapingService.scrape_url(req.url, req.mode, req.max_items)

@router.post("/export")
def export_scraped(data: list, format_type: str = "csv", current_user: User = Depends(get_current_user)):
    content, filename = ScrapingService.export_scraped_data(data, format_type)
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(content=content, media_type="application/octet-stream", headers=headers)
