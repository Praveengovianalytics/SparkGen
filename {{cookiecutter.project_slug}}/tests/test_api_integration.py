import json
import pytest


try:
    from fastapi.testclient import TestClient  # type: ignore
    from {{ cookiecutter.project_slug }}.api.app import app  # type: ignore
except Exception:
    TestClient = None  # type: ignore[misc]
    app = None  # type: ignore[misc]


@pytest.mark.skipif(TestClient is None or app is None, reason="FastAPI app not available in this template mode.")
def test_agent_invoke_endpoint_returns_json_structure():
    client = TestClient(app)
    response = client.post("/agent/invoke", json={"query": "hello"})
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "result" in body
