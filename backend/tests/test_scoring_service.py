from app.models import PlayerRoleHint
from app.services.scoring_service import (
    calculate_scores_for_player,
    calculate_weighted_overall,
    compute_role_hint,
    normalize_higher_better,
    normalize_lower_better,
)


def test_normalize_higher_better_scales_between_zero_and_one() -> None:
    assert normalize_higher_better(15, 10, 20) == 0.5


def test_normalize_lower_better_inverts_range() -> None:
    assert normalize_lower_better(4, 2, 6) == 0.5


def test_compute_role_hint_detects_all_rounder() -> None:
    assert compute_role_hint(3.7, 5.0, 4.0) == PlayerRoleHint.ALL_ROUNDER


def test_compute_role_hint_detects_batter_using_new_cutoff() -> None:
    assert compute_role_hint(3.7, 4.9, 3.0) == PlayerRoleHint.BATTER


def test_compute_role_hint_detects_bowler_using_new_cutoff() -> None:
    assert compute_role_hint(3.6, 5.0, 3.0) == PlayerRoleHint.BOWLER


def test_compute_role_hint_detects_fielding_asset_using_new_cutoff() -> None:
    assert compute_role_hint(3.0, 4.0, 4.0) == PlayerRoleHint.FIELDING_ASSET


def test_calculate_scores_for_player_returns_scores_out_of_ten() -> None:
    player_input = {
        "has_batting": True,
        "has_bowling": True,
        "has_fielding": True,
        "batting_innings": 10,
        "batting_fours": 20.0,
        "batting_strike_rate": 150.0,
        "batting_average": 40.0,
        "bowling_overs": 12.0,
        "bowling_economy": 6.5,
        "bowling_average": 18.0,
        "fielding_catches_per_match": 0.8,
        "fielding_direct_run_outs_per_match": 0.3,
        "fielding_indirect_run_outs_per_match": 0.1,
    }
    metric_ranges = {
        "batting_fours": (0.0, 25.0),
        "batting_strike_rate": (90.0, 160.0),
        "batting_average": (5.0, 50.0),
        "bowling_economy": (4.0, 12.0),
        "bowling_average": (10.0, 35.0),
        "fielding_catches_per_match": (0.0, 1.0),
        "fielding_direct_run_outs_per_match": (0.0, 0.5),
        "fielding_indirect_run_outs_per_match": (0.0, 0.4),
    }

    scores = calculate_scores_for_player(player_input, metric_ranges)

    assert 0.0 <= scores["batting_score"] <= 10.0
    assert 0.0 <= scores["bowling_score"] <= 10.0
    assert 0.0 <= scores["fielding_score"] <= 10.0
    assert 0.0 <= scores["overall_score"] <= 10.0


def test_calculate_weighted_overall_renormalizes_when_batting_missing() -> None:
    overall = calculate_weighted_overall(
        {
            "batting": None,
            "bowling": 8.0,
            "fielding": 6.0,
        }
    )

    assert overall == 7.33


def test_calculate_scores_sets_batting_to_zero_when_innings_is_7_or_less() -> None:
    player_input = {
        "has_batting": True,
        "has_bowling": True,
        "has_fielding": True,
        "batting_innings": 7,
        "batting_fours": 20.0,
        "batting_strike_rate": 150.0,
        "batting_average": 40.0,
        "bowling_overs": 12.0,
        "bowling_economy": 6.5,
        "bowling_average": 18.0,
        "fielding_catches_per_match": 0.8,
        "fielding_direct_run_outs_per_match": 0.3,
        "fielding_indirect_run_outs_per_match": 0.1,
    }
    metric_ranges = {
        "batting_fours": (0.0, 25.0),
        "batting_strike_rate": (90.0, 160.0),
        "batting_average": (5.0, 50.0),
        "bowling_economy": (4.0, 12.0),
        "bowling_average": (10.0, 35.0),
        "fielding_catches_per_match": (0.0, 1.0),
        "fielding_direct_run_outs_per_match": (0.0, 0.5),
        "fielding_indirect_run_outs_per_match": (0.0, 0.4),
    }

    scores = calculate_scores_for_player(player_input, metric_ranges)

    assert scores["batting_score"] == 0.0


def test_calculate_scores_sets_bowling_to_zero_when_overs_is_7_or_less() -> None:
    player_input = {
        "has_batting": True,
        "has_bowling": True,
        "has_fielding": True,
        "batting_innings": 10,
        "batting_fours": 20.0,
        "batting_strike_rate": 150.0,
        "batting_average": 40.0,
        "bowling_overs": 7.0,
        "bowling_economy": 6.5,
        "bowling_average": 18.0,
        "fielding_catches_per_match": 0.8,
        "fielding_direct_run_outs_per_match": 0.3,
        "fielding_indirect_run_outs_per_match": 0.1,
    }
    metric_ranges = {
        "batting_fours": (0.0, 25.0),
        "batting_strike_rate": (90.0, 160.0),
        "batting_average": (5.0, 50.0),
        "bowling_economy": (4.0, 12.0),
        "bowling_average": (10.0, 35.0),
        "fielding_catches_per_match": (0.0, 1.0),
        "fielding_direct_run_outs_per_match": (0.0, 0.5),
        "fielding_indirect_run_outs_per_match": (0.0, 0.4),
    }

    scores = calculate_scores_for_player(player_input, metric_ranges)

    assert scores["bowling_score"] == 0.0
