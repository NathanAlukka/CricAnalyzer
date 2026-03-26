from __future__ import annotations

from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, joinedload

from app.core.scoring_config import (
    MINIMUM_SAMPLE_LIMITS,
    ROLE_HINT_THRESHOLDS,
    SCORE_SCALE_MAX,
    SCORING_VERSION,
    SCORING_WEIGHTS,
)
from app.models import MergedPlayerScore, Player, PlayerRoleHint


def round_score(value: float) -> float:
    return round(max(0.0, min(SCORE_SCALE_MAX, value)), 2)


def normalize_higher_better(value: float, minimum: float, maximum: float) -> float:
    if maximum <= minimum:
        return 0.0
    return (value - minimum) / (maximum - minimum)


def normalize_lower_better(value: float, minimum: float, maximum: float) -> float:
    if maximum <= minimum:
        return 0.0
    return (maximum - value) / (maximum - minimum)


def scale_to_ten(value: float) -> float:
    return round_score(value * SCORE_SCALE_MAX)


def safe_rate(total: float, matches: int) -> float:
    if matches <= 0:
        return 0.0
    return total / matches


def compute_role_hint(
    batting_score: float | None,
    bowling_score: float | None,
    fielding_score: float | None,
) -> PlayerRoleHint:
    batting_value = batting_score or 0.0
    bowling_value = bowling_score or 0.0
    fielding_value = fielding_score or 0.0

    if batting_score is not None and bowling_score is not None:
        if batting_value >= ROLE_HINT_THRESHOLDS["all_rounder_min"] and bowling_value >= ROLE_HINT_THRESHOLDS["all_rounder_min"]:
            return PlayerRoleHint.ALL_ROUNDER
    if fielding_score is not None:
        if fielding_value >= ROLE_HINT_THRESHOLDS["fielding_asset_min"] and fielding_value > batting_value and fielding_value > bowling_value:
            return PlayerRoleHint.FIELDING_ASSET
    if batting_score is not None and batting_value >= bowling_value + ROLE_HINT_THRESHOLDS["specialist_gap"]:
        return PlayerRoleHint.BATTER
    if bowling_score is not None and bowling_value >= batting_value + ROLE_HINT_THRESHOLDS["specialist_gap"]:
        return PlayerRoleHint.BOWLER
    if batting_score is not None or bowling_score is not None:
        return PlayerRoleHint.ALL_ROUNDER
    return PlayerRoleHint.FIELDING_ASSET if fielding_score is not None else PlayerRoleHint.UNKNOWN


def build_metric_ranges(player_inputs: list[dict]) -> dict[str, tuple[float, float]]:
    metric_names = {
        "batting_fours": [],
        "batting_strike_rate": [],
        "batting_average": [],
        "bowling_economy": [],
        "bowling_average": [],
        "fielding_catches_per_match": [],
        "fielding_direct_run_outs_per_match": [],
        "fielding_indirect_run_outs_per_match": [],
    }

    for item in player_inputs:
        if item["has_batting"]:
            metric_names["batting_fours"].append(item["batting_fours"])
            metric_names["batting_strike_rate"].append(item["batting_strike_rate"])
            metric_names["batting_average"].append(item["batting_average"])
        if item["has_bowling"]:
            metric_names["bowling_economy"].append(item["bowling_economy"])
            metric_names["bowling_average"].append(item["bowling_average"])
        if item["has_fielding"]:
            metric_names["fielding_catches_per_match"].append(item["fielding_catches_per_match"])
            metric_names["fielding_direct_run_outs_per_match"].append(item["fielding_direct_run_outs_per_match"])
            metric_names["fielding_indirect_run_outs_per_match"].append(item["fielding_indirect_run_outs_per_match"])

    return {
        name: (min(values), max(values)) if values else (0.0, 0.0)
        for name, values in metric_names.items()
    }


def extract_latest_stat(stats: list) -> object | None:
    if not stats:
        return None
    return stats[-1]


def prepare_player_inputs(players: list[Player]) -> list[dict]:
    prepared: list[dict] = []

    for player in players:
        batting = extract_latest_stat(player.batting_stats)
        bowling = extract_latest_stat(player.bowling_stats)
        fielding = extract_latest_stat(player.fielding_stats)

        fielding_matches = int(fielding.matches) if fielding else 0

        prepared.append(
            {
                "player": player,
                "has_batting": batting is not None,
                "has_bowling": bowling is not None,
                "has_fielding": fielding is not None,
                "batting_innings": int(getattr(batting, "innings", 0)) if batting else 0,
                "batting_fours": float(batting.fours) if batting else 0.0,
                "batting_strike_rate": float(batting.strike_rate or 0) if batting else 0.0,
                "batting_average": float(batting.average or 0) if batting else 0.0,
                "bowling_overs": float(getattr(bowling, "overs", 0) or 0) if bowling else 0.0,
                "bowling_economy": float(bowling.economy or 0) if bowling else 0.0,
                "bowling_average": float(bowling.average or 0) if bowling else 0.0,
                "fielding_catches_per_match": safe_rate(float(fielding.catches), fielding_matches) if fielding else 0.0,
                "fielding_direct_run_outs_per_match": safe_rate(float(fielding.direct_run_outs), fielding_matches) if fielding else 0.0,
                "fielding_indirect_run_outs_per_match": safe_rate(float(fielding.indirect_run_outs), fielding_matches) if fielding else 0.0,
            }
        )

    return prepared


def calculate_weighted_overall(component_scores: dict[str, float | None]) -> float:
    overall_weights = SCORING_WEIGHTS["overall"]
    active_components = {
        name: score
        for name, score in component_scores.items()
        if score is not None
    }

    if not active_components:
        return 0.0

    active_weight_total = sum(overall_weights[name] for name in active_components)
    weighted_total = sum(
        active_components[name] * (overall_weights[name] / active_weight_total)
        for name in active_components
    )
    return round_score(weighted_total)


def calculate_scores_for_player(player_input: dict, metric_ranges: dict[str, tuple[float, float]]) -> dict:
    batting_weights = SCORING_WEIGHTS["batting"]
    bowling_weights = SCORING_WEIGHTS["bowling"]
    fielding_weights = SCORING_WEIGHTS["fielding"]

    batting_score: float | None = None
    if player_input["has_batting"]:
        batting_fours = normalize_higher_better(player_input["batting_fours"], *metric_ranges["batting_fours"])
        batting_sr = normalize_higher_better(player_input["batting_strike_rate"], *metric_ranges["batting_strike_rate"])
        batting_avg = normalize_higher_better(player_input["batting_average"], *metric_ranges["batting_average"])
        batting_score = scale_to_ten(
            batting_fours * batting_weights["fours"]
            + batting_sr * batting_weights["strike_rate"]
            + batting_avg * batting_weights["average"]
        )
        if player_input["batting_innings"] <= MINIMUM_SAMPLE_LIMITS["batting_innings_max_zero_score"]:
            batting_score = 0.0

    bowling_score: float | None = None
    if player_input["has_bowling"]:
        bowling_econ = normalize_lower_better(player_input["bowling_economy"], *metric_ranges["bowling_economy"])
        bowling_avg = normalize_lower_better(player_input["bowling_average"], *metric_ranges["bowling_average"])
        bowling_score = scale_to_ten(
            bowling_econ * bowling_weights["economy"]
            + bowling_avg * bowling_weights["average"]
        )
        if player_input["bowling_overs"] <= MINIMUM_SAMPLE_LIMITS["bowling_overs_max_zero_score"]:
            bowling_score = 0.0

    fielding_score: float | None = None
    if player_input["has_fielding"]:
        fielding_catches = normalize_higher_better(player_input["fielding_catches_per_match"], *metric_ranges["fielding_catches_per_match"])
        fielding_direct = normalize_higher_better(player_input["fielding_direct_run_outs_per_match"], *metric_ranges["fielding_direct_run_outs_per_match"])
        fielding_indirect = normalize_higher_better(player_input["fielding_indirect_run_outs_per_match"], *metric_ranges["fielding_indirect_run_outs_per_match"])
        fielding_score = scale_to_ten(
            fielding_catches * fielding_weights["catches_per_match"]
            + fielding_direct * fielding_weights["direct_run_outs_per_match"]
            + fielding_indirect * fielding_weights["indirect_run_outs_per_match"]
        )

    overall_score = calculate_weighted_overall(
        {
            "batting": batting_score,
            "bowling": bowling_score,
            "fielding": fielding_score,
        }
    )

    role_hint = compute_role_hint(batting_score, bowling_score, fielding_score)

    return {
        "batting_score": batting_score,
        "bowling_score": bowling_score,
        "fielding_score": fielding_score,
        "overall_score": overall_score,
        "role_hint": role_hint,
    }


def process_player_scores(session: Session) -> dict[str, int | str]:
    players = list(
        session.scalars(
            select(Player).options(
                joinedload(Player.batting_stats),
                joinedload(Player.bowling_stats),
                joinedload(Player.fielding_stats),
            )
        ).unique()
    )

    prepared_players = prepare_player_inputs(players)
    metric_ranges = build_metric_ranges(prepared_players)

    session.execute(delete(MergedPlayerScore))

    scores_created = 0
    for player_input in prepared_players:
        scores = calculate_scores_for_player(player_input, metric_ranges)
        session.add(
            MergedPlayerScore(
                player_id=player_input["player"].id,
                batting_score=Decimal(str(scores["batting_score"] or 0.0)),
                bowling_score=Decimal(str(scores["bowling_score"] or 0.0)),
                fielding_score=Decimal(str(scores["fielding_score"] or 0.0)),
                overall_score=Decimal(str(scores["overall_score"])),
                role_hint=scores["role_hint"],
                scoring_version=SCORING_VERSION,
            )
        )
        scores_created += 1

    session.commit()

    return {
        "players_processed": len(prepared_players),
        "scores_created": scores_created,
        "scoring_version": SCORING_VERSION,
    }
