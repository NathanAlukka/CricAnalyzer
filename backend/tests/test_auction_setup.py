from fastapi.testclient import TestClient

from app.db.session import SessionLocal
from app.main import app
from app.models import Player, Team, TeamRoster
from app.schemas.auction_setup import AuctionSettingsSaveRequest, CaptainSetupItem
from app.services.auction_setup_service import save_auction_setup

client = TestClient(app)


def test_get_auction_setup_defaults():
    response = client.get("/api/auction-setup")

    assert response.status_code == 200
    data = response.json()
    assert "tournament_name" in data
    assert data["number_of_teams"] >= 2
    assert "teams" in data


def test_save_auction_setup_retains_linked_captain():
    session = SessionLocal()
    try:
        session.query(TeamRoster).delete()
        session.query(Team).delete()
        existing_player = session.query(Player).filter(Player.name == "captain test player").one_or_none()
        if existing_player is not None:
            session.delete(existing_player)
            session.commit()

        player = Player(name="captain test player", display_name="Captain Test Player")
        session.add(player)
        session.commit()
        session.refresh(player)

        payload = AuctionSettingsSaveRequest(
            tournament_name="Captain Setup Test",
            number_of_teams=2,
            squad_size=12,
            total_points_per_captain=100,
            captain_self_value_deduction=15,
            max_bid=25,
            teams=[
                CaptainSetupItem(
                    team_name="Team Alpha",
                    owner_name="Owner A",
                    captain_name="Captain Test Player",
                    captain_player_id=player.id,
                    is_my_team=True,
                ),
                CaptainSetupItem(
                    team_name="Team Beta",
                    owner_name="Owner B",
                    captain_name="Captain Beta",
                    captain_player_id=None,
                    is_my_team=False,
                ),
            ],
        )

        save_auction_setup(session, payload)

        team = session.query(Team).filter(Team.name == "Team Alpha").one()
        roster_entry = session.query(TeamRoster).filter(TeamRoster.team_id == team.id).one()

        assert roster_entry.player_id == player.id
        assert roster_entry.status.value == "captain_retained"
    finally:
        session.close()
