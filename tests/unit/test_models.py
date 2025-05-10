import pytest
from api.models.schemas import ExplainRequest, GenerateRequest, LearnRequest, APIResponse

def test_explain_request_model():
    request = ExplainRequest(
        code="def test(): pass",
        language="python",
        difficulty="beginner",
        focus_areas=["syntax", "best_practices"],
        line_by_line=True,
        include_examples=True
    )
    assert request.code == "def test(): pass"
    assert request.language == "python"
    assert request.difficulty == "beginner"
    assert "syntax" in request.focus_areas
    assert request.line_by_line is True
    assert request.provider == "groq"  # Test default provider

def test_generate_request_model():
    request = GenerateRequest(
        prompt="Create a sorting algorithm",
        language="python",
        context="Using quicksort",
        constraints=["O(n log n)", "in-place"]
    )
    assert request.prompt == "Create a sorting algorithm"
    assert request.language == "python"
    assert request.context == "Using quicksort"
    assert "O(n log n)" in request.constraints

def test_learn_request_model():
    previous_context = [
        {"role": "user", "content": "What are decorators?"},
        {"role": "assistant", "content": "Decorators are..."}
    ]
    request = LearnRequest(
        topic="Python decorators",
        difficulty="advanced",
        format="interactive",
        previous_context=previous_context
    )
    assert request.topic == "Python decorators"
    assert request.difficulty == "advanced"
    assert len(request.previous_context) == 2

def test_api_response_model():
    response = APIResponse(
        success=True,
        data={"result": "Test output"},
        error=None
    )
    assert response.success is True
    assert response.data["result"] == "Test output"
    assert response.error is None

def test_api_response_with_error():
    response = APIResponse(
        success=False,
        data={},
        error="Test error message"
    )
    assert response.success is False
    assert response.error == "Test error message"