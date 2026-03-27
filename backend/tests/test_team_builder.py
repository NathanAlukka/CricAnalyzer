from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_team_builder():
    response = client.get("/api/team-builder")

    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "roster" in data
