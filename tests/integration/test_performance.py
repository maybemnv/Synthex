import pytest
import asyncio
import time
from httpx import AsyncClient
from api.services.llm_provider import LLMProvider

@pytest.mark.asyncio
async def test_api_response_time():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        start_time = time.time()
        response = await client.get("/api/status")
        end_time = time.time()
        
        assert (end_time - start_time) < 1.0  # Response under 1 second
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_concurrent_requests():
    async with AsyncClient(base_url="http://localhost:8000") as client:
        tasks = [client.get("/api/status") for _ in range(5)]
        responses = await asyncio.gather(*tasks)
        assert all(r.status_code == 200 for r in responses)

@pytest.mark.asyncio
async def test_response_time(mock_env_vars, mock_groq_response, mocker):
    # Mock the API call
    mock_client = mocker.AsyncMock()
    mock_client.post.return_value.json.return_value = mock_groq_response
    mock_client.post.return_value.raise_for_status = mocker.Mock()
    
    mocker.patch("httpx.AsyncClient", return_value=mock_client)
    
    provider = LLMProvider()
    start_time = time.time()
    
    messages = [{"role": "user", "content": "test"}]
    await provider.generate_completion(messages)
    
    end_time = time.time()
    response_time = end_time - start_time
    
    assert response_time < 1.0, f"Response time {response_time:.2f}s exceeded 1s threshold"