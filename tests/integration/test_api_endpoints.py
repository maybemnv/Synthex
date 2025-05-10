import pytest
from fastapi.testclient import TestClient
from api.models.schemas import ExplainRequest, GenerateRequest, LearnRequest
from httpx import AsyncClient
import asyncio
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_status_endpoint():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        response = await client.get("/api/status")
        assert response.status_code == 200
        assert response.json()["success"] == True

@pytest.mark.asyncio
async def test_explain_endpoint(client, mocker):
    # Mock the LLMProvider.generate_completion method
    async def mock_generate_completion(messages, max_tokens=1000):
        return {"choices": [{"message": {"content": "This is an explanation."}}]}
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_generate_completion
    )

    payload = {
        "code": "print('Hello, world!')",
        "language": "python",
        "difficulty": "beginner"
    }
    response = client.post("/api/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "explanation" in data["data"]

@pytest.mark.asyncio
async def test_generate_endpoint(client, mocker):
    async def mock_generate_completion(messages, max_tokens=1000):
        return {"choices": [{"message": {"content": "def add(a, b): return a + b"}}]}
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_generate_completion
    )

    payload = {
        "prompt": "Create a function that adds two numbers",
        "language": "python"
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "generated_code" in data["data"]

@pytest.mark.asyncio
async def test_learn_endpoint(client, mocker):
    async def mock_generate_completion(messages, max_tokens=1000):
        return {"choices": [{"message": {"content": "This is a lesson about decorators."}}]}
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_generate_completion
    )

    payload = {
        "topic": "Python decorators",
        "subtopic": "basics",
        "format": "tutorial"
    }
    response = client.post("/api/learn", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "lesson" in data["data"]

@pytest.mark.asyncio
async def test_error_handling(client, mock_env_vars, mocker):
    async def mock_completion(*args, **kwargs):
        raise Exception("Test error")
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_completion
    )
    response = client.post(
        "/api/explain",
        json={
            "code": "def test(): pass",
            "language": "python"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["error"] is not None

@pytest.mark.asyncio
async def test_explain_endpoint_success(client, mocker):
    mock_response = {
        "choices": [{"message": {"content": "This code prints 'Hello World'"}}]
    }
    
    async def mock_completion(*args, **kwargs):
        return mock_response
        
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_completion
    )
    
    payload = {
        "code": "print('Hello World')",
        "language": "python",
        "difficulty": "beginner",
        "focus_areas": ["syntax", "logic"],
        "line_by_line": True,
        "include_examples": True
    }
    
    response = client.post("/api/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "explanation" in data["data"]

@pytest.mark.asyncio
async def test_generate_endpoint_success(client, mocker):
    mock_response = {
        "choices": [{"message": {"content": "def add(a, b): return a + b"}}]
    }
    
    async def mock_completion(*args, **kwargs):
        return mock_response
        
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_completion
    )
    
    payload = {
        "prompt": "Create a function that adds two numbers",
        "language": "python",
        "context": "Math operations",
        "optimization": "speed",
        "include_comments": True
    }
    
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "generated_code" in data["data"]

# Error cases
@pytest.mark.asyncio
async def test_explain_endpoint_error(client, mocker):
    async def mock_completion(*args, **kwargs):
        raise Exception("API Error")
        
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_completion
    )
    
    payload = {
        "code": "print('Hello World')",
        "language": "python"
    }
    
    response = client.post("/api/explain", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] is not None

@pytest.mark.asyncio
async def test_generate_endpoint_error(client, mocker):
    async def mock_completion(*args, **kwargs):
        raise Exception("API Error")
        
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_completion
    )
    
    payload = {
        "prompt": "Invalid prompt",
        "language": "python"
    }
    
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] is not None

@pytest.mark.asyncio
async def test_learn_endpoint_error(client, mocker):
    async def mock_generate_completion(*args, **kwargs):
        raise Exception("Simulated error")
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_generate_completion
    )
    payload = {
        "topic": "Python decorators",
        "subtopic": "basics",
        "format": "tutorial"
    }
    response = client.post("/api/learn", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"] is not None