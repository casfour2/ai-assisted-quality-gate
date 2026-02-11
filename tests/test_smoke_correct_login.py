import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.smoke
def test_login_happypath():
    response = client.post("/login", json={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {"token": "fake-jwt-token"}