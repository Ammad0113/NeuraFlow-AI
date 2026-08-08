from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_rag_upload_and_query():
    # Login first
    login_res = client.post("/api/auth/login", json={
        "email": "demo@neuraflow.ai",
        "password": "demo123456"
    })
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Upload document
    sample_text = "NeuraFlow AI handles enterprise retrieval augmented generation with instant vector indexing."
    files = {"file": ("test_doc.txt", sample_text.encode(), "text/plain")}
    
    up_res = client.post("/api/rag/upload", files=files, headers=headers)
    assert up_res.status_code == 200
    assert up_res.json()["filename"] == "test_doc.txt"

    # Query RAG
    query_res = client.post("/api/rag/query", json={"query": "vector indexing", "top_k": 2}, headers=headers)
    assert query_res.status_code == 200
    assert len(query_res.json()["citations"]) > 0
