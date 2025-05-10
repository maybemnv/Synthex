import pytest
import os
import sys
from fastapi import HTTPException
from api.services.llm_provider import LLMProvider

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

@pytest.mark.asyncio
async def test_llm_provider_initialization(mock_env_vars):
    provider = LLMProvider()
    assert provider.api_key == "test_key_123"
    assert provider.api_base == "https://api.groq.com/openai/v1"
    assert provider.model == "llama3-8b-8192"

@pytest.mark.asyncio
async def test_generate_completion_success(mock_env_vars, mocker):
    provider = LLMProvider()
    mock_response = {
        "choices": [{"message": {"content": "Test response"}}]
    }

    class MockResponse:
        def raise_for_status(self):
            pass
        def json(self):
            return mock_response

    class MockAsyncClient:
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
        async def post(self, *args, **kwargs):
            return MockResponse()

    mocker.patch("httpx.AsyncClient", return_value=MockAsyncClient())
    result = await provider.generate_completion([{"role": "user", "content": "test"}])
    assert result == mock_response

@pytest.mark.asyncio
async def test_generate_completion_api_error(mock_env_vars, mocker):
    provider = LLMProvider()

    class MockAsyncClient:
        async def __aenter__(self):
            raise Exception("Simulated API error")
        async def __aexit__(self, exc_type, exc, tb):
            pass

    mocker.patch("httpx.AsyncClient", return_value=MockAsyncClient())
    with pytest.raises(HTTPException) as exc_info:
        await provider.generate_completion([{"role": "user", "content": "test"}])
    assert "LLM API Error" in str(exc_info.value.detail)