from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_post_auction_analysis():
    response = client.get("/api/post-auction-analysis")

    assert response.status_code == 200
    data = response.json()
    assert "teams" in data
    assert "contender_team_names" in data
    assert "best_value_buys" in data
