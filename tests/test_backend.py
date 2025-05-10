from fastapi.testclient import TestClient
from main import app

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