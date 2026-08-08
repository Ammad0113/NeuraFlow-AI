import requests
from typing import Dict, Any, Optional

BACKEND_URL = "http://localhost:8008/api"

class APIClient:
    @staticmethod
    def _get_headers(token: Optional[str] = None) -> Dict[str, str]:
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @staticmethod
    def post(endpoint: str, data: Optional[dict] = None, json: Optional[dict] = None, files: Optional[dict] = None, token: Optional[str] = None) -> requests.Response:
        url = f"{BACKEND_URL}{endpoint}"
        return requests.post(url, data=data, json=json, files=files, headers=APIClient._get_headers(token))

    @staticmethod
    def get(endpoint: str, params: Optional[dict] = None, token: Optional[str] = None) -> requests.Response:
        url = f"{BACKEND_URL}{endpoint}"
        return requests.get(url, params=params, headers=APIClient._get_headers(token))
