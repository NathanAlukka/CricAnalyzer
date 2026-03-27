from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MergedPlayerScore, Player, SoldPlayer, Team, TeamRoster
from app.services.live_auction_service import build_team_summary


def describe_strengths_and_weaknesses(team_summary: dict, averages: dict[str, float]) -> tuple[list[str], list[str]]:
    labels = {
        "batting_total": "batting",
        "bowling_total": "bowling",
        "fielding_total": "fielding",
        "overall_total": "overall balance",
    }

    strengths: list[str] = []
    weaknesses: list[str] = []

    for key, label in labels.items():
        average_value = averages.get(key, 0.0)
        if average_value <= 0:
            continue

        current_value = float(team_summary[key])
        if current_value >= average_value * 1.05:
            strengths.append(f"Above-average {label}")
        elif current_value <= average_value * 0.95:
            weaknesses.append(f"Below-average {label}")

    if not strengths:
        strengths.append("Balanced profile")
    if not weaknesses:
        weaknesses.append("No major weakness yet")

    return strengths, weaknesses


def get_post_auction_analysis(session: Session) -> dict:
    teams = session.scalars(select(Team).order_by(Team.id.asc())).all()
    if not teams:
        return {
            "teams": [],
            "contender_team_names": [],
            "average_team_overall": 0.0,
            "best_value_buys": [],
        }

    team_summaries: list[dict] = []
    for team in teams:
        summary = build_team_summary(session, team)
        roster_entries = session.scalars(select(TeamRoster).where(TeamRoster.team_id == team.id)).all()

        scored_players: list[dict] = []
        for entry in roster_entries:
            player = session.get(Player, entry.player_id)
            merged_score = session.scalar(select(MergedPlayerScore).where(MergedPlayerScore.player_id == entry.player_id))
            if player is None or merged_score is None:
                continue
            scored_players.append(
                {
                    "player_name": player.display_name or player.name,
                    "overall_score": float(merged_score.overall_score),
                }
            )

        scored_players.sort(key=lambda item: item["overall_score"], reverse=True)
        team_summaries.append(
            {
                "team_id": team.id,
                "team_name": team.name,
                "owner_name": team.owner_name,
                "players_count": len(roster_entries),
                **summary,
                "top_players": scored_players[:3],
            }
        )

    averages = {
        "batting_total": sum(team["batting_total"] for team in team_summaries) / len(team_summaries),
        "bowling_total": sum(team["bowling_total"] for team in team_summaries) / len(team_summaries),
        "fielding_total": sum(team["fielding_total"] for team in team_summaries) / len(team_summaries),
        "overall_total": sum(team["overall_total"] for team in team_summaries) / len(team_summaries),
    }

    analyzed_teams: list[dict] = []
    for team_summary in sorted(team_summaries, key=lambda item: item["overall_total"], reverse=True):
        strengths, weaknesses = describe_strengths_and_weaknesses(team_summary, averages)
        analyzed_teams.append(
            {
                "team_id": team_summary["team_id"],
                "team_name": team_summary["team_name"],
                "owner_name": team_summary["owner_name"],
                "players_count": team_summary["players_count"],
                "remaining_budget": team_summary["remaining_budget"],
                "batting_total": team_summary["batting_total"],
                "bowling_total": team_summary["bowling_total"],
                "fielding_total": team_summary["fielding_total"],
                "overall_total": team_summary["overall_total"],
                "batter_count": team_summary["batter_count"],
                "bowler_count": team_summary["bowler_count"],
                "all_rounder_count": team_summary["all_rounder_count"],
                "fielding_asset_count": team_summary["fielding_asset_count"],
                "strengths": strengths,
                "weaknesses": weaknesses,
                "top_players": team_summary["top_players"],
            }
        )

    contender_team_names = [team["team_name"] for team in analyzed_teams[: min(2, len(analyzed_teams))]]

    sold_entries = session.scalars(select(SoldPlayer).order_by(SoldPlayer.sold_price.asc())).all()
    best_value_buys: list[dict] = []
    for sold_entry in sold_entries:
        player = session.get(Player, sold_entry.player_id)
        team = session.get(Team, sold_entry.team_id)
        merged_score = session.scalar(select(MergedPlayerScore).where(MergedPlayerScore.player_id == sold_entry.player_id))
        if player is None or team is None or merged_score is None:
            continue

        sold_price = float(sold_entry.sold_price)
        if sold_price <= 0:
            continue

        overall_score = float(merged_score.overall_score)
        best_value_buys.append(
            {
                "player_name": player.display_name or player.name,
                "team_name": team.name,
                "sold_price": sold_price,
                "overall_score": overall_score,
                "value_index": round(overall_score / sold_price, 3),
            }
        )

    best_value_buys.sort(key=lambda item: item["value_index"], reverse=True)

    return {
        "teams": analyzed_teams,
        "contender_team_names": contender_team_names,
        "average_team_overall": round(averages["overall_total"], 2),
        "best_value_buys": best_value_buys[:10],
    }
