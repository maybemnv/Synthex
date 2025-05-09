import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

@pytest.mark.asyncio
async def test_status_endpoint(test_client):
    response = test_client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@pytest.mark.asyncio
async def test_explain_endpoint(test_client, sample_code):
    response = test_client.post(
        "/api/explain",
        json={
            "code": sample_code,
            "language": "python",
            "difficulty": "beginner"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True

@pytest.mark.asyncio
async def test_generate_endpoint(test_client):
    response = test_client.post(
        "/api/generate",
        json={
            "prompt": "Create a function that adds two numbers",
            "language": "python"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True

@pytest.mark.asyncio
async def test_interactive_endpoint(test_client):
    response = test_client.post(
        "/api/interactive",
        json={
            "topic": "linked lists",
            "subtopic": "insertion",
            "format": "tutorial",
            "difficulty": "intermediate"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] == True

@pytest.mark.asyncio
async def test_error_handling(test_client):
    response = test_client.post(
        "/api/explain",
        json={
            "code": "",  # Empty code should trigger error
            "language": "python"
        }
    )
    assert response.status_code == 400