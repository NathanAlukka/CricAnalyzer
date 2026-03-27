from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MergedPlayerScore, Player, Team, TeamRoster
from app.services.live_auction_service import build_team_summary


def get_team_builder_data(session: Session) -> dict:
    my_team = session.scalar(select(Team).where(Team.is_my_team.is_(True)))
    if my_team is None:
        return {"summary": None, "roster": []}

    roster_entries = session.scalars(
        select(TeamRoster).where(TeamRoster.team_id == my_team.id).order_by(TeamRoster.id.asc())
    ).all()

    roster_items: list[dict] = []
    for entry in roster_entries:
        player = session.get(Player, entry.player_id)
        score = session.scalar(select(MergedPlayerScore).where(MergedPlayerScore.player_id == entry.player_id))
        roster_items.append(
            {
                "player_id": entry.player_id,
                "player_name": player.display_name or player.name if player else "Unknown player",
                "role_hint": score.role_hint.value if score else "unknown",
                "roster_status": entry.status.value,
                "purchase_price": float(entry.purchase_price) if entry.purchase_price is not None else None,
                "batting_score": float(score.batting_score) if score else 0.0,
                "bowling_score": float(score.bowling_score) if score else 0.0,
                "fielding_score": float(score.fielding_score) if score else 0.0,
                "overall_score": float(score.overall_score) if score else 0.0,
            }
        )

    return {
        "summary": build_team_summary(session, my_team),
        "roster": roster_items,
    }
