from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_ml_pipeline():
    login_res = client.post("/api/auth/login", json={
        "email": "demo@neuraflow.ai",
        "password": "demo123456"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    with open("sample_data/sample_sales.csv", "rb") as f:
        file_bytes = f.read()

    files = {"file": ("sample_sales.csv", file_bytes, "text/csv")}
    data = {
        "target_column": "Churn_Risk",
        "task_type": "classification",
        "algorithm": "random_forest",
        "test_size": 0.2
    }

    train_res = client.post("/api/ml/train", files=files, data=data, headers=headers)
    assert train_res.status_code == 200
    model_info = train_res.json()
    assert "model_id" in model_info
    assert "accuracy" in model_info["metrics"]
