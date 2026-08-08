from fastapi.testclient import TestClient
from backend.main import app
from backend.database import init_db

init_db()
client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_login_demo_user():
    response = client.post("/api/auth/login", json={
        "email": "demo@neuraflow.ai",
        "password": "demo123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "demo@neuraflow.ai"
