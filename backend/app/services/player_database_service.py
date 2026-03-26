from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import MergedPlayerScore, Player


def get_player_database(session: Session, search: str | None = None, role_hint: str | None = None) -> list[dict]:
    query = (
        select(Player, MergedPlayerScore)
        .join(MergedPlayerScore, MergedPlayerScore.player_id == Player.id)
        .order_by(MergedPlayerScore.overall_score.desc(), Player.name.asc())
    )

    if search:
        query = query.where(Player.name.ilike(f"%{search.strip()}%"))

    if role_hint:
        query = query.where(MergedPlayerScore.role_hint == role_hint)

    rows = session.execute(query).all()

    return [
        {
            "id": player.id,
            "name": player.display_name or player.name,
            "team_name": player.team_name,
            "role_hint": merged_score.role_hint.value,
            "batting_score": float(merged_score.batting_score),
            "bowling_score": float(merged_score.bowling_score),
            "fielding_score": float(merged_score.fielding_score),
            "overall_score": float(merged_score.overall_score),
        }
        for player, merged_score in rows
    ]
