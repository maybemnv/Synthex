import pytest
from api import ExplainRequest, GenerateRequest, LearnRequest

def test_explain_request_model():
    request = ExplainRequest(
        code="def test(): pass",
        language="python"
    )
    assert request.difficulty == "intermediate"
    assert "algorithm" in request.focus_areas

def test_generate_request_model():
    request = GenerateRequest(
        prompt="Create a sorting algorithm",
        language="python"
    )
    assert request.optimization == "balanced"
    assert request.include_comments == True