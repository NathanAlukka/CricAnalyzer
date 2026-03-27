from __future__ import annotations

import math

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.scoring_config import BID_RECOMMENDATION_CONFIG, ROLE_HINT_THRESHOLDS
from app.models import CurrentPlayerPool, MergedPlayerScore, Player, PoolStatus, Team, TeamRoster
from app.services.live_auction_service import build_team_summary


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def _load_roster_scores(session: Session, player_ids: list[int]) -> list[MergedPlayerScore]:
    if not player_ids:
        return []
    return session.scalars(
        select(MergedPlayerScore).where(MergedPlayerScore.player_id.in_(player_ids))
    ).all()


def _get_team_needs(session: Session, my_team: Team) -> set[str]:
    roster_entries = session.scalars(select(TeamRoster).where(TeamRoster.team_id == my_team.id)).all()
    player_ids = [entry.player_id for entry in roster_entries]
    roster_scores = _load_roster_scores(session, player_ids)
    current_batters = sum(1 for score in roster_scores if float(score.batting_score) >= ROLE_HINT_THRESHOLDS["batter_min"])
    current_bowlers = sum(1 for score in roster_scores if float(score.bowling_score) >= ROLE_HINT_THRESHOLDS["bowler_min"])

    target_batters = max(1, math.ceil((my_team.squad_size_target or 12) * BID_RECOMMENDATION_CONFIG["target_batting_ratio"]))
    target_bowlers = min(BID_RECOMMENDATION_CONFIG["target_bowlers"], my_team.squad_size_target or BID_RECOMMENDATION_CONFIG["target_bowlers"])
    needs: set[str] = set()
    if current_batters < target_batters:
        needs.add("batting")
    if current_bowlers < target_bowlers:
        needs.add("bowling")
    needs.add("fielding")
    return needs


def _calculate_need_multiplier(session: Session, my_team: Team, target_score: MergedPlayerScore) -> tuple[float, float]:
    team_needs = _get_team_needs(session, my_team)
    is_target_batter = float(target_score.batting_score) >= ROLE_HINT_THRESHOLDS["batter_min"]
    is_target_bowler = float(target_score.bowling_score) >= ROLE_HINT_THRESHOLDS["bowler_min"]
    is_target_fielder = float(target_score.fielding_score) >= ROLE_HINT_THRESHOLDS["fielding_asset_min"]
    player_matches = 0
    if "batting" in team_needs and is_target_batter:
        player_matches += 1
    if "bowling" in team_needs and is_target_bowler:
        player_matches += 1
    if "fielding" in team_needs and is_target_fielder:
        player_matches += 1

    if not team_needs:
        return 0.0, 0.0

    need_count = len(team_needs)
    multiplier = round(player_matches / need_count, 2)
    return multiplier, multiplier


def _derive_label(fair_value: float, hard_cap: float, team_need_score: float) -> tuple[str, str]:
    if fair_value >= BID_RECOMMENDATION_CONFIG["priority_target_min"] and team_need_score >= 0.66:
        return "priority target", "This player covers most of your current needs and is worth pushing for strongly."
    if fair_value >= BID_RECOMMENDATION_CONFIG["good_value_min"] and team_need_score >= 0.5:
        return "good pick", "This is a solid fit for your squad and a good player to actively consider."
    if team_need_score >= 0.33:
        return "50/50", "The player helps part of what your team needs, but the price should decide the move."
    if hard_cap > BID_RECOMMENDATION_CONFIG["skip_max"]:
        return "not at the moment", "This player is usable, but your current team priorities suggest waiting for a better fit."
    return "skip", "This player does not match enough of your current needs to justify spending here."


def get_bid_recommendation(session: Session, player_id: int) -> dict:
    target_score = session.scalar(select(MergedPlayerScore).where(MergedPlayerScore.player_id == player_id))
    if target_score is None:
        raise ValueError("Player score not found for recommendation.")

    pool_entry = session.scalar(select(CurrentPlayerPool).where(CurrentPlayerPool.player_id == player_id))
    if pool_entry is None:
        raise ValueError("Player is not in the current player pool.")

    player = session.get(Player, player_id)
    my_team = session.scalar(select(Team).where(Team.is_my_team.is_(True)))
    if my_team is None:
        raise ValueError("No team is marked as my team in auction setup.")

    team_summary = build_team_summary(session, my_team)
    open_slots = max(team_summary["open_slots"], 1)
    remaining_budget = float(my_team.remaining_budget)
    average_spend_per_slot = remaining_budget / open_slots
    need_multiplier, team_need_score = _calculate_need_multiplier(session, my_team, target_score)
    base_value = average_spend_per_slot * need_multiplier
    score_bonus = (
        float(target_score.batting_score)
        + float(target_score.bowling_score)
        + float(target_score.fielding_score)
    ) * BID_RECOMMENDATION_CONFIG["score_bonus_multiplier"]
    fair_value = base_value + score_bonus

    budget_safety_cap = remaining_budget * BID_RECOMMENDATION_CONFIG["budget_safety_ratio"]
    hard_cap = min(
        fair_value * BID_RECOMMENDATION_CONFIG["hard_cap_markup"],
        remaining_budget,
        float(my_team.max_bid_limit) if my_team.max_bid_limit is not None else remaining_budget,
        budget_safety_cap,
    )

    reserve_floor = float(pool_entry.reserve_price) if pool_entry.reserve_price is not None else 0.0
    fair_value = max(fair_value, reserve_floor)
    fair_value = round(fair_value, 2)
    hard_cap = round(max(hard_cap, reserve_floor), 2)
    good_buy_upto = round(min(fair_value * BID_RECOMMENDATION_CONFIG["good_buy_discount"], hard_cap), 2)
    overpay_threshold = round(min(fair_value * BID_RECOMMENDATION_CONFIG["overpay_markup"], hard_cap), 2)

    label, reason = _derive_label(fair_value, hard_cap, team_need_score)

    return {
        "player_id": player_id,
        "player_name": player.display_name or player.name if player else "Unknown player",
        "fair_value": fair_value,
        "good_buy_upto": good_buy_upto,
        "overpay_threshold": overpay_threshold,
        "hard_cap": hard_cap,
        "recommendation_label": label,
        "recommendation_reason": reason,
        "scarcity_score": 0.0,
        "team_need_score": team_need_score,
    }
