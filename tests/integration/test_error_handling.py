import os
import pytest
from fastapi import HTTPException
from api.services.llm_provider import LLMProvider

def test_invalid_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GROQ_API_KEY not found"):
        LLMProvider()

async def test_invalid_request_body(client):
    response = client.post(
        "/api/generate",
        json={
            "invalid_field": "test"
        }
    )
    
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_error_handling(client):
    response = client.post(
        "/api/explain",
        json={
            "code": "",
            "language": "python"
        }
    )
    assert response.json()["success"] is False
    assert response.json()["error"] is not None