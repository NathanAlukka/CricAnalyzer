from app.db.base import Base
from app.models import (
    AuctionEvent,
    AuctionSetting,
    BattingStat,
    BowlingStat,
    Captain,
    CurrentPlayerPool,
    FieldingStat,
    MergedPlayerScore,
    Player,
    SoldPlayer,
    Team,
    TeamRoster,
)


def test_expected_tables_exist_in_metadata() -> None:
    expected_tables = {
        "players",
        "batting_stats",
        "bowling_stats",
        "fielding_stats",
        "merged_player_scores",
        "auction_settings",
        "captains",
        "teams",
        "team_rosters",
        "auction_events",
        "sold_players",
        "current_player_pool",
    }

    # Touch imported models so they are not treated as unused.
    assert all(
        model is not None
        for model in (
            Player,
            BattingStat,
            BowlingStat,
            FieldingStat,
            MergedPlayerScore,
            AuctionSetting,
            Captain,
            Team,
            TeamRoster,
            AuctionEvent,
            SoldPlayer,
            CurrentPlayerPool,
        )
    )
    assert expected_tables.issubset(Base.metadata.tables.keys())
