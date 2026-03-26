from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    AuctionEvent,
    AuctionEventType,
    AuctionSetting,
    Captain,
    CurrentPlayerPool,
    MergedPlayerScore,
    Player,
    PoolStatus,
    SoldPlayer,
    Team,
    TeamRoster,
)
from app.models import RosterStatus
from app.schemas.live_auction import SubmitAuctionEventRequest


def get_active_auction_setting(session: Session) -> AuctionSetting | None:
    return session.scalar(
        select(AuctionSetting).where(AuctionSetting.is_active.is_(True)).order_by(AuctionSetting.created_at.desc())
    )


def build_team_summary(session: Session, team: Team) -> dict:
    roster_entries = session.scalars(select(TeamRoster).where(TeamRoster.team_id == team.id)).all()
    player_ids = [entry.player_id for entry in roster_entries]
    merged_scores = session.scalars(select(MergedPlayerScore).where(MergedPlayerScore.player_id.in_(player_ids))).all() if player_ids else []

    batting_total = sum(float(score.batting_score) for score in merged_scores)
    bowling_total = sum(float(score.bowling_score) for score in merged_scores)
    fielding_total = sum(float(score.fielding_score) for score in merged_scores)
    overall_total = sum(float(score.overall_score) for score in merged_scores)

    return {
        "team_name": team.name,
        "remaining_budget": float(team.remaining_budget),
        "squad_size_target": team.squad_size_target,
        "players_bought": len(roster_entries),
        "open_slots": max((team.squad_size_target or 0) - len(roster_entries), 0),
        "batting_total": round(batting_total, 2),
        "bowling_total": round(bowling_total, 2),
        "fielding_total": round(fielding_total, 2),
        "overall_total": round(overall_total, 2),
    }


def get_live_auction_state(session: Session) -> dict:
    pool_entries = session.scalars(
        select(CurrentPlayerPool)
        .where(CurrentPlayerPool.status == PoolStatus.AVAILABLE)
        .order_by(CurrentPlayerPool.id.asc())
    ).all()
    pool_entries = sorted(
        pool_entries,
        key=lambda entry: (entry.auction_order is None, entry.auction_order or 0, entry.id),
    )

    remaining_pool: list[dict] = []
    for entry in pool_entries:
        player = session.get(Player, entry.player_id)
        merged_score = session.scalar(select(MergedPlayerScore).where(MergedPlayerScore.player_id == entry.player_id))
        remaining_pool.append(
            {
                "player_id": entry.player_id,
                "player_name": player.display_name or player.name,
                "team_name": player.team_name,
                "role_hint": merged_score.role_hint.value if merged_score else "unknown",
                "batting_score": float(merged_score.batting_score) if merged_score else 0.0,
                "bowling_score": float(merged_score.bowling_score) if merged_score else 0.0,
                "fielding_score": float(merged_score.fielding_score) if merged_score else 0.0,
                "overall_score": float(merged_score.overall_score) if merged_score else 0.0,
                "is_captain": entry.is_captain,
                "reserve_price": float(entry.reserve_price) if entry.reserve_price is not None else None,
                "auction_order": entry.auction_order,
            }
        )

    teams = session.scalars(select(Team).order_by(Team.id.asc())).all()
    team_items = []
    my_team_summary = None
    for team in teams:
        roster_count = session.query(TeamRoster).filter(TeamRoster.team_id == team.id).count()
        team_items.append(
            {
                "team_id": team.id,
                "team_name": team.name,
                "owner_name": team.owner_name,
                "remaining_budget": float(team.remaining_budget),
                "squad_size_target": team.squad_size_target,
                "players_bought": roster_count,
                "is_my_team": team.is_my_team,
            }
        )
        if team.is_my_team:
            my_team_summary = build_team_summary(session, team)

    recent_events = session.scalars(select(AuctionEvent).order_by(AuctionEvent.id.desc()).limit(20)).all()
    event_items = []
    for event in recent_events:
        player = session.get(Player, event.player_id) if event.player_id else None
        team = session.get(Team, event.team_id) if event.team_id else None
        event_items.append(
            {
                "event_id": event.id,
                "player_name": player.display_name or player.name if player else "Unknown player",
                "team_name": team.name if team else None,
                "event_type": event.event_type.value,
                "final_price": float(event.final_price) if event.final_price is not None else None,
                "nomination_order": event.nomination_order,
            }
        )

    return {
        "remaining_pool": remaining_pool,
        "teams": team_items,
        "my_team_summary": my_team_summary,
        "recent_events": event_items,
    }


def reset_live_auction(session: Session) -> dict:
    session.query(SoldPlayer).delete()
    session.query(TeamRoster).delete()
    session.query(AuctionEvent).delete()

    pool_entries = session.scalars(select(CurrentPlayerPool)).all()
    for entry in pool_entries:
        entry.status = PoolStatus.AVAILABLE

    teams = session.scalars(select(Team)).all()
    for team in teams:
        captain = session.scalar(select(Captain).where(Captain.team_id == team.id))
        deduction = float(captain.self_cost_deduction) if captain else 0.0
        team.remaining_budget = Decimal(str(float(team.starting_budget) - deduction))

    session.commit()
    return {"message": "Auction state reset successfully."}


def submit_live_auction_event(session: Session, payload: SubmitAuctionEventRequest) -> dict:
    pool_entry = session.scalar(select(CurrentPlayerPool).where(CurrentPlayerPool.player_id == payload.player_id))
    if pool_entry is None:
        raise ValueError("Player is not in the current player pool.")
    if pool_entry.status != PoolStatus.AVAILABLE:
        raise ValueError("Player has already been processed in the auction.")

    active_setting = get_active_auction_setting(session)
    next_nomination_order = session.query(AuctionEvent).count() + 1

    team_id = payload.team_id
    if payload.event_type == "bought_by_me":
        my_team = session.scalar(select(Team).where(Team.is_my_team.is_(True)))
        if my_team is None:
            raise ValueError("No team is marked as my team in auction setup.")
        team_id = my_team.id

    event = AuctionEvent(
        auction_setting_id=active_setting.id if active_setting else None,
        player_id=payload.player_id,
        team_id=team_id,
        nomination_order=next_nomination_order,
        final_price=Decimal(str(payload.final_price)) if payload.final_price is not None else None,
        event_type=AuctionEventType(payload.event_type),
        notes=payload.notes,
    )
    session.add(event)
    session.flush()

    if payload.event_type == "unsold":
        pool_entry.status = PoolStatus.UNSOLD
    else:
        if team_id is None:
            raise ValueError("A team must be selected when the player is sold.")
        if payload.final_price is None:
            raise ValueError("Final price is required when the player is sold.")

        team = session.get(Team, team_id)
        if team is None:
            raise ValueError("Selected team was not found.")
        if float(team.remaining_budget) < payload.final_price:
            raise ValueError("Selected team does not have enough remaining budget.")

        team.remaining_budget = Decimal(str(float(team.remaining_budget) - payload.final_price))
        pool_entry.status = PoolStatus.SOLD

        roster_entry = TeamRoster(
            team_id=team.id,
            player_id=payload.player_id,
            purchase_price=Decimal(str(payload.final_price)),
            status=RosterStatus.BOUGHT,
        )
        session.add(roster_entry)

        sold_player = SoldPlayer(
            auction_event_id=event.id,
            player_id=payload.player_id,
            team_id=team.id,
            sold_price=Decimal(str(payload.final_price)),
        )
        session.add(sold_player)

    session.commit()
    return {"message": "Auction event saved successfully."}
