import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.smoke
def test_ui_page_loads():
    response = client.get("/ui")
    assert response.status_code == 200
    assert "AI QA Demo Dashboard" in response.text