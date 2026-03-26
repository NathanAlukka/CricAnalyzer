from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_auction_setup_defaults():
    response = client.get("/api/auction-setup")

    assert response.status_code == 200
    data = response.json()
    assert data["tournament_name"] == "Cricket Auction"
    assert data["number_of_teams"] >= 2
    assert "teams" in data
