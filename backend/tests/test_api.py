"""
test_api.py
-----------
Integration tests for FastAPI endpoints.
Mocks the internal logic services (Agent & Guardrails).
"""

from fastapi.testclient import TestClient
from unittest.mock import patch
from src.app import app

client = TestClient(app)

def test_health_check():
    """Verify the health endpoint works."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

@patch("src.app.brand_agent.generate")
@patch("src.app.brand_guard.evaluate")
def test_generate_content_flow(mock_evaluate, mock_generate):
    """
    Test the full generation flow:
    Request -> Agent -> Guardrails -> Response
    """
    # 1. Setup Mocks
    mock_generate.return_value = {
        "content": "Draft content...",
        "used_references": ["ref1", "ref2"]
    }
    mock_evaluate.return_value = {
        "score": 95,
        "reasoning": "Excellent tone."
    }

    # 2. Make Request
    payload = {
        "topic": "Test Topic",
        "content_type": "Email",
        "tone_modifier": "Neutral"
    }
    response = client.post("/api/v1/generate", json=payload)

    # 3. Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Draft content..."
    assert data["brand_score"] == 95
    assert data["used_references"] == ["ref1", "ref2"]