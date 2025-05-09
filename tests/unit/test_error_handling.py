import pytest
from fastapi import HTTPException

async def test_invalid_api_key(client):
    # Remove API key from environment
    os.environ.pop("GROQ_API_KEY", None)
    
    response = client.post(
        "/api/explain",
        json={
            "code": "def test(): pass",
            "language": "python"
        }
    )
    
    assert response.status_code == 500
    assert "GROQ_API_KEY not found" in response.json()["error"]

async def test_invalid_request_body(client):
    response = client.post(
        "/api/generate",
        json={
            "invalid_field": "test"
        }
    )
    
    assert response.status_code == 422