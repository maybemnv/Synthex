import pytest
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_learn_endpoint_success(client, mock_env_vars, mocker):
    async def mock_completion(*args, **kwargs):
        return {"choices": [{"message": {"content": "Learning content"}}]}
    mocker.patch(
        "api.services.llm_provider.LLMProvider.generate_completion",
        side_effect=mock_completion
    )
    response = client.post(
        "/api/learn",
        json={
            "topic": "Python decorators",
            "difficulty": "intermediate",
            "format": "interactive"
        }
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "data" in response.json()

@pytest.mark.asyncio
async def test_learn_endpoint_error(client, mocker):
    async def mock_generate_completion(*args, **kwargs):
        raise Exception("Test error")
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