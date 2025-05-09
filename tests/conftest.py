import pytest
from fastapi.testclient import TestClient
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api import app

@pytest.fixture
def test_client():
    from api import app
    return TestClient(app)

@pytest.fixture
def mock_groq_response():
    return {
        "choices": [{
            "message": {
                "content": "Test response content"
            }
        }]
    }

@pytest.fixture
def sample_code():
    return """
    def hello_world():
        print("Hello, World!")
    """

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Automatically mock environment variables for all tests"""
    os.environ["GROQ_API_KEY"] = "test_key_123"
    yield
    os.environ.pop("GROQ_API_KEY", None)