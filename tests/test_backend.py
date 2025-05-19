import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from fastapi.testclient import TestClient
from main import app
import pytest
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_status():
    resp = client.get("/api/status")
    assert resp.status_code == 200
    assert resp.json()["success"] is True

def test_explain_success():
    payload = {
        "code": "print('hi')",
        "language": "python",
        "focus_areas": ["Algorithm Steps"],
        "difficulty": "Beginner",
        "include_examples": True,
        "line_by_line": False
    }
    resp = client.post("/api/explain", json=payload)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    assert "data" in resp.json()

def test_explain_missing_code():
    payload = {
        "language": "python",
        "focus_areas": ["Algorithm Steps"],
        "difficulty": "Beginner",
        "include_examples": True,
        "line_by_line": False
    }
    resp = client.post("/api/explain", json=payload)
    assert resp.status_code == 422

def test_generate_success():
    payload = {
        "description": "Print hello",
        "language": "python",
        "difficulty": "Beginner"
    }
    resp = client.post("/api/generate", json=payload)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    assert "data" in resp.json()

def test_generate_missing_description():
    payload = {
        "language": "python",
        "difficulty": "Beginner"
    }
    resp = client.post("/api/generate", json=payload)
    assert resp.status_code == 422

def test_learn_success():
    payload = {
        "main_topic": "loops",
        "language": "python",
        "difficulty": "Beginner"
    }
    resp = client.post("/api/learn", json=payload)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    assert "data" in resp.json()

def test_learn_missing_main_topic():
    payload = {
        "language": "python",
        "difficulty": "Beginner"
    }
    resp = client.post("/api/learn", json=payload)
    assert resp.status_code == 422

def test_code_flow_success():
    payload = {
        "code": """
        def factorial(n):
            if n == 0:
                return 1
            return n * factorial(n-1)
        """
    }
    resp = client.post("/api/visualization/code-flow", json=payload)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    data = resp.json()["data"]
    assert "nodes" in data
    assert "edges" in data

def test_code_flow_missing_code():
    resp = client.post("/api/visualization/code-flow", json={})
    assert resp.status_code == 422

def test_algorithm_visualization_success():
    payload = {
        "code": """
        def bubble_sort(arr):
            n = len(arr)
            for i in range(n):
                for j in range(0, n-i-1):
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
        """,
        "input_data": [5, 2, 9, 1]
    }
    resp = client.post("/api/visualization/algorithm-visualization", json=payload)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    data = resp.json()["data"]
    assert "steps" in data
    assert "complexity" in data

def test_algorithm_visualization_missing_input():
    payload = {"code": "def sort(arr): pass"}
    resp = client.post("/api/visualization/algorithm-visualization", json=payload)
    assert resp.status_code == 422

def test_performance_comparison_success():
    payload = {
        "codes": {
            "bubble_sort": """
            def bubble_sort(arr):
                n = len(arr)
                for i in range(n):
                    for j in range(0, n-i-1):
                        if arr[j] > arr[j+1]:
                            arr[j], arr[j+1] = arr[j+1], arr[j]
            """,
            "insertion_sort": """
            def insertion_sort(arr):
                for i in range(1, len(arr)):
                    key = arr[i]
                    j = i-1
                    while j >= 0 and key < arr[j]:
                        arr[j+1] = arr[j]
                        j -= 1
                    arr[j+1] = key
            """
        },
        "input_sizes": [10, 100, 1000]
    }
    resp = client.post("/api/visualization/performance-comparison", json=payload)
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    data = resp.json()["data"]
    assert "algorithms" in data

def test_performance_comparison_missing_codes():
    payload = {"input_sizes": [10, 100]}
    resp = client.post("/api/visualization/performance-comparison", json=payload)
    assert resp.status_code == 422

def test_llm_provider_initialization():
    from api.services.llm_provider import LLMProvider
    provider = LLMProvider()
    assert provider.api_base == "https://api.groq.com/openai/v1"
    assert provider.model == "llama3-8b-8192"

def test_llm_provider_extract_json():
    from api.services.llm_provider import LLMProvider
    provider = LLMProvider()
    json_str = '{"test": "value"}'
    result = provider._extract_json(json_str)
    assert result == '{"test": "value"}'

def test_llm_provider_serialize_messages():
    from api.services.llm_provider import LLMProvider
    from langchain_core.messages import SystemMessage, HumanMessage
    provider = LLMProvider()
    messages = [
        SystemMessage(content="system msg"),
        HumanMessage(content="human msg")
    ]
    result = provider._serialize_messages(messages)
    assert len(result) == 2
    assert result[0]["role"] == "system"
    assert result[1]["role"] == "user"

def test_visualization_invalid_code():
    payload = {"code": ""}
    resp = client.post("/api/visualization/code-flow", json=payload)
    assert resp.status_code == 200
    assert resp.json()["success"] is False
    assert "error" in resp.json()

def test_visualization_malformed_input():
    payload = {"code": 123}  # Invalid type
    resp = client.post("/api/visualization/code-flow", json=payload)
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_llm_provider_generate_completion():
    from api.services.llm_provider import LLMProvider
    provider = LLMProvider()
    messages = [{"role": "user", "content": "test"}]
    try:
        result = await provider.generate_completion(messages)
        assert isinstance(result, str)
    except Exception as e:
        assert "API Error" in str(e)

def test_algorithm_visualization_invalid_input():
    payload = {
        "code": "def sort(arr): pass",
        "input_data": "not a list"  # Invalid input type
    }
    resp = client.post("/api/visualization/algorithm-visualization", json=payload)
    assert resp.status_code == 422

def test_performance_comparison_invalid_sizes():
    payload = {
        "codes": {"test": "def test(): pass"},
        "input_sizes": ["invalid"]  # Invalid sizes
    }
    resp = client.post("/api/visualization/performance-comparison", json=payload)
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_visualization_endpoints():
    # Test code flow analysis
    code_flow_payload = {
        "code": "def test(): pass"
    }
    response = client.post("/api/visualization/code-flow", json=code_flow_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "nodes" in data["data"]
    assert "edges" in data["data"]

    # Test algorithm visualization
    algo_viz_payload = {
        "code": "def bubble_sort(arr): pass",
        "input_data": [5, 2, 9, 1]
    }
    response = client.post("/api/visualization/algorithm-visualization", json=algo_viz_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "steps" in data["data"]
    assert "complexity" in data["data"]

    # Test performance comparison
    perf_payload = {
        "codes": {
            "bubble": "def bubble_sort(arr): pass",
            "quick": "def quick_sort(arr): pass"
        },
        "input_sizes": [10, 100, 1000]
    }
    response = client.post("/api/visualization/performance-comparison", json=perf_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "algorithms" in data["data"]

@pytest.mark.asyncio
async def test_visualization_error_handling():
    # Test empty code
    response = client.post("/api/visualization/code-flow", json={"code": ""})
    assert response.status_code == 200
    assert response.json()["success"] is False

    # Test invalid input data
    response = client.post("/api/visualization/algorithm-visualization", 
                          json={"code": "def test(): pass", "input_data": "invalid"})
    assert response.status_code == 422

    # Test missing algorithms
    response = client.post("/api/visualization/performance-comparison", 
                          json={"codes": {}, "input_sizes": [10]})
    assert response.status_code == 200
    assert response.json()["success"] is False

@pytest.mark.asyncio
async def test_llm_provider_methods():
    with patch('api.services.llm_provider.LLMProvider.generate_completion') as mock_completion:
        mock_completion.return_value = '{"test": "response"}'
        
        from api.services.llm_provider import LLMProvider
        provider = LLMProvider()
        
        # Test code flow analysis
        result = await provider.analyze_code_flow("def test(): pass")
        assert isinstance(result, dict)
        
        # Test algorithm visualization
        result = await provider.visualize_algorithm_steps("def sort(): pass", [1,2,3])
        assert isinstance(result, dict)
        
        # Test performance comparison
        result = await provider.compare_algorithm_performance(
            {"test": "def test(): pass"}, 
            [10]
        )
        assert isinstance(result, dict)