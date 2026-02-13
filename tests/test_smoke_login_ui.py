import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.smoke
def test_ui_contains_login_form(client):
    response = client.get("/ui")
    assert response.status_code == 200
    assert 'id="username"' in response.text
    assert 'id="password"' in response.text
    assert "Login" in response.text