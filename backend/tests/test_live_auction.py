from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_live_auction_state():
    response = client.get("/api/live-auction/state")

    assert response.status_code == 200
    data = response.json()
    assert "remaining_pool" in data
    assert "teams" in data
    assert "recent_events" in data
