from app.services.historical_data_service import deduplicate_rows


def test_deduplicate_batting_rows_keeps_best_single_row_per_player() -> None:
    rows = [
        {
            "player_name": "Nathan Alukka",
            "matches": 3,
            "runs": 20,
            "average": 10.0,
            "strike_rate": 90.0,
            "fours": 1,
        },
        {
            "player_name": "Nathan Alukka",
            "matches": 5,
            "runs": 40,
            "average": 20.0,
            "strike_rate": 120.0,
            "fours": 4,
        },
        {
            "player_name": "Another Player",
            "matches": 4,
            "runs": 30,
            "average": 15.0,
            "strike_rate": 110.0,
            "fours": 2,
        },
    ]

    deduplicated = deduplicate_rows("batting", rows)
    deduplicated_by_name = {row["player_name"]: row for row in deduplicated}

    assert len(deduplicated) == 2
    assert deduplicated_by_name["Nathan Alukka"]["matches"] == 5
    assert deduplicated_by_name["Nathan Alukka"]["runs"] == 40
