import pytest
from httpx import AsyncClient
import asyncio

@pytest.mark.asyncio
async def test_status_endpoint():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/api/status")
        assert response.status_code == 200
        assert response.json()["success"] == True

@pytest.mark.asyncio
async def test_explain_endpoint():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.post(
            "/api/explain",
            json={
                "code": "def test(): pass",
                "language": "python"
            }
        )
        assert response.status_code == 200

async def test_generate_endpoint(client, mock_groq_response, monkeypatch):
    async def mock_generate(*args, **kwargs):
        return "def generated_code(): pass"
    
    monkeypatch.setattr("api.LLMProvider.generate_response", mock_generate)
    
    response = client.post(
        "/api/generate",
        json={
            "prompt": "Create a simple function",
            "language": "python"
        }
    )
    
    assert response.status_code == 200
    assert "code" in response.json()["data"]