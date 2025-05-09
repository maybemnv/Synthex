import pytest
import os
import sys
from fastapi import HTTPException

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from api import LLMProvider

@pytest.mark.asyncio
async def test_llm_provider_initialization():
    # Test with valid API key
    os.environ["GROQ_API_KEY"] = "test_key"
    provider = LLMProvider()
    assert provider.model == "llama3-8b-8192"
    assert provider.api_base == "https://api.groq.com/openai/v1"

    # Test with missing API key
    os.environ.pop("GROQ_API_KEY")
    with pytest.raises(HTTPException):
        LLMProvider()

@pytest.mark.asyncio
async def test_generate_response():
    provider = LLMProvider()
    response = await provider.generate_response(
        "Explain what this code does: print('hello')",
        temperature=0.7,
        max_tokens=100
    )
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.asyncio
async def test_provider_error_handling():
    # Test with invalid API key
    os.environ["GROQ_API_KEY"] = "invalid_key"
    provider = LLMProvider()
    
    with pytest.raises(HTTPException):
        await provider.generate_response("test prompt")