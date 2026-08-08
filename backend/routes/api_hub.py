from fastapi import APIRouter, Depends
from backend.routes.auth import get_current_user
from backend.database.models import User
from backend.models.api_hub import GenericAPIRequest
from backend.services.api_hub_service import APIHubService

router = APIRouter(prefix="/api-hub", tags=["API Integration Hub"])

@router.get("/weather")
def get_weather(city: str = "San Francisco", current_user: User = Depends(get_current_user)):
    return APIHubService.get_weather(city)

@router.get("/currency")
def get_currency(base: str = "USD", current_user: User = Depends(get_current_user)):
    return APIHubService.get_currency_rates(base)

@router.get("/github")
def get_github(owner: str = "fastapi", repo: str = "fastapi", current_user: User = Depends(get_current_user)):
    return APIHubService.get_github_repo(owner, repo)

@router.post("/execute")
def execute_generic(req: GenericAPIRequest, current_user: User = Depends(get_current_user)):
    return APIHubService.execute_generic_request(req.url, req.method, req.headers, req.body)
