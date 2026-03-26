from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import BattingStat, BowlingStat, FieldingStat, MergedPlayerScore, Player


def get_player_detail(session: Session, player_id: int) -> dict | None:
    player = session.scalar(
        select(Player)
        .where(Player.id == player_id)
        .options(
            selectinload(Player.batting_stats),
            selectinload(Player.bowling_stats),
            selectinload(Player.fielding_stats),
            selectinload(Player.merged_scores),
        )
    )
    if player is None or not player.merged_scores:
        return None

    merged_score = player.merged_scores[-1]
    batting = player.batting_stats[-1] if player.batting_stats else None
    bowling = player.bowling_stats[-1] if player.bowling_stats else None
    fielding = player.fielding_stats[-1] if player.fielding_stats else None

    averages = session.execute(
        select(
            func.avg(MergedPlayerScore.batting_score),
            func.avg(MergedPlayerScore.bowling_score),
            func.avg(MergedPlayerScore.fielding_score),
            func.avg(MergedPlayerScore.overall_score),
        )
    ).one()
    batting_averages = session.execute(
        select(
            func.avg(BattingStat.matches),
            func.avg(BattingStat.runs),
            func.avg(BattingStat.average),
            func.avg(BattingStat.strike_rate),
            func.avg(BattingStat.fours),
        )
    ).one()
    bowling_averages = session.execute(
        select(
            func.avg(BowlingStat.matches),
            func.avg(BowlingStat.wickets),
            func.avg(BowlingStat.average),
            func.avg(BowlingStat.economy),
        )
    ).one()
    fielding_averages = session.execute(
        select(
            func.avg(FieldingStat.matches),
            func.avg(FieldingStat.catches),
            func.avg(FieldingStat.direct_run_outs),
            func.avg(FieldingStat.indirect_run_outs),
        )
    ).one()

    return {
        "id": player.id,
        "name": player.display_name or player.name,
        "team_name": player.team_name,
        "role_hint": merged_score.role_hint.value,
        "batting_score": float(merged_score.batting_score),
        "bowling_score": float(merged_score.bowling_score),
        "fielding_score": float(merged_score.fielding_score),
        "overall_score": float(merged_score.overall_score),
        "batting_stats": (
            {
                "matches": batting.matches,
                "runs": batting.runs,
                "average": float(batting.average or 0),
                "strike_rate": float(batting.strike_rate or 0),
                "fours": batting.fours,
            }
            if batting
            else None
        ),
        "bowling_stats": (
            {
                "matches": bowling.matches,
                "wickets": bowling.wickets,
                "average": float(bowling.average or 0),
                "economy": float(bowling.economy or 0),
            }
            if bowling
            else None
        ),
        "fielding_stats": (
            {
                "matches": fielding.matches,
                "catches": fielding.catches,
                "direct_run_outs": fielding.direct_run_outs,
                "indirect_run_outs": fielding.indirect_run_outs,
            }
            if fielding
            else None
        ),
        "batting_average_stats": {
            "matches": int(round(float(batting_averages[0] or 0))),
            "runs": int(round(float(batting_averages[1] or 0))),
            "average": float(batting_averages[2] or 0),
            "strike_rate": float(batting_averages[3] or 0),
            "fours": int(round(float(batting_averages[4] or 0))),
        },
        "bowling_average_stats": {
            "matches": int(round(float(bowling_averages[0] or 0))),
            "wickets": int(round(float(bowling_averages[1] or 0))),
            "average": float(bowling_averages[2] or 0),
            "economy": float(bowling_averages[3] or 0),
        },
        "fielding_average_stats": {
            "matches": int(round(float(fielding_averages[0] or 0))),
            "catches": int(round(float(fielding_averages[1] or 0))),
            "direct_run_outs": int(round(float(fielding_averages[2] or 0))),
            "indirect_run_outs": int(round(float(fielding_averages[3] or 0))),
        },
        "player_scores": {
            "batting_score": float(merged_score.batting_score),
            "bowling_score": float(merged_score.bowling_score),
            "fielding_score": float(merged_score.fielding_score),
            "overall_score": float(merged_score.overall_score),
        },
        "average_scores": {
            "batting_score": float(averages[0] or 0),
            "bowling_score": float(averages[1] or 0),
            "fielding_score": float(averages[2] or 0),
            "overall_score": float(averages[3] or 0),
        },
    }
