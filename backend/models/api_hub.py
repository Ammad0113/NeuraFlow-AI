from pydantic import BaseModel
from typing import Optional, Dict, Any

class GenericAPIRequest(BaseModel):
    url: str
    method: str = "GET" # GET, POST
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None

class IntegrationResponse(BaseModel):
    service_name: str
    status_code: int
    data: Any
