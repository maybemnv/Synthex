import pytest
from fastapi.testclient import TestClient
from main import app  # Import from main.py instead of api
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

@pytest.fixture
def client():    # Changed from test_client to client
    return TestClient(app)

@pytest.fixture
def mock_response():
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
    original_key = os.getenv("GROQ_API_KEY")
    os.environ["GROQ_API_KEY"] = "test_key_123"
    yield
    if original_key:
        os.environ["GROQ_API_KEY"] = original_key
    else:
        del os.environ["GROQ_API_KEY"]