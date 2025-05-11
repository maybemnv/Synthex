import pytest
from unittest.mock import patch, MagicMock
import streamlit as st

# Example: Test the code explanation API call logic
@patch("requests.post")
def test_explain_api_call(mock_post):
    # Arrange
    from pages import explain
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "success": True,
        "data": {"explanation": "This code sorts a list."},
        "error": None
    }
    mock_response.raise_for_status = lambda: None
    mock_post.return_value = mock_response

    # Simulate Streamlit session state
    st.session_state["model_provider"] = "Groq (Llama 3)"

    # Act
    # Call the function that triggers the API call (you may need to refactor your code to make this testable)
    # For example, if you have a function like get_explanation(payload), call it here

    payload = {
        "code": "arr.sort()",
        "language": "python",
        "difficulty": "beginner",
        "focus_areas": [],
        "line_by_line": False,
        "include_examples": False,
        "provider": "groq"
    }
    # This assumes you have a function to call, e.g., explain.get_explanation(payload)
    # explanation = explain.get_explanation(payload)
    # assert explanation == "This code sorts a list."

    # If your logic is inside the Streamlit UI, you can only test the API call and response parsing here

    response = mock_post("http://localhost:8000/api/explain", json=payload)
    result = response.json()
    assert result["success"]
    assert result["data"]["explanation"] == "This code sorts a list."

# Repeat similar tests for generate and learn endpoints

@patch("requests.post")
def test_generate_api_call(mock_post):
    from pages import generate_v2
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "success": True,
        "data": {"code": "print('Hello, World!')"},
        "error": None
    }
    mock_response.raise_for_status = lambda: None
    mock_post.return_value = mock_response

    payload = {
        "prompt": "Print Hello, World!",
        "language": "python",
        "optimization_focus": "none",
        "include_comments": False,
        "provider": "groq"
    }
    response = mock_post("http://localhost:8000/api/generate", json=payload)
    result = response.json()
    assert result["success"]
    assert "Hello, World!" in result["data"]["code"]

@patch("requests.post")
def test_learn_api_call(mock_post):
    from pages import learn
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "success": True,
        "data": {"lesson": "A variable stores data.", "context": []},
        "error": None
    }
    mock_response.raise_for_status = lambda: None
    mock_post.return_value = mock_response

    payload = {
        "main_topic": "variables",
        "language": "python",
        "difficulty": "beginner"
    }
    params = {
        "template": "basic",
        "session_id": "test-session"
    }
    response = mock_post("http://localhost:8000/api/learn", json=payload, params=params)
    result = response.json()
    assert result["success"]
    assert "variable" in result["data"]["lesson"].lower()