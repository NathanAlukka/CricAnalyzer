from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import (
    AuctionEvent,
    AuctionSetting,
    Captain,
    CurrentPlayerPool,
    Player,
    PoolStatus,
    RosterStatus,
    SoldPlayer,
    Team,
    TeamRoster,
)
from app.schemas.auction_setup import AuctionSettingsSaveRequest
from app.services.excel_parser import normalize_player_name, parse_current_player_pool_excel


def get_player_options(session: Session) -> list[dict]:
    players = session.scalars(select(Player).order_by(Player.name.asc())).all()
    return [{"id": player.id, "name": player.display_name or player.name} for player in players]


def get_auction_setup(session: Session) -> dict:
    active_setting = session.scalar(
        select(AuctionSetting).where(AuctionSetting.is_active.is_(True)).order_by(AuctionSetting.created_at.desc())
    )

    if active_setting is None:
        return {
            "tournament_name": "Cricket Auction",
            "number_of_teams": 6,
            "squad_size": 12,
            "total_points_per_captain": 100.0,
            "captain_self_value_deduction": 0.0,
            "max_bid": 25.0,
            "teams": [],
        }

    teams = session.scalars(
        select(Team).where(Team.auction_setting_id == active_setting.id).order_by(Team.id.asc())
    ).all()

    team_items: list[dict] = []
    for team in teams:
        captain = session.scalar(select(Captain).where(Captain.team_id == team.id))
        team_items.append(
            {
                "team_name": team.name,
                "owner_name": team.owner_name,
                "captain_name": captain.captain_name if captain else "",
                "captain_player_id": captain.player_id if captain else None,
                "is_my_team": team.is_my_team,
            }
        )

    return {
        "tournament_name": active_setting.tournament_name,
        "number_of_teams": active_setting.number_of_teams,
        "squad_size": active_setting.squad_size,
        "total_points_per_captain": float(active_setting.total_points_per_captain),
        "captain_self_value_deduction": float(active_setting.captain_self_value_deduction),
        "max_bid": float(active_setting.max_bid),
        "teams": team_items,
    }


def save_auction_setup(session: Session, payload: AuctionSettingsSaveRequest) -> dict:
    existing_settings = session.scalars(select(AuctionSetting).where(AuctionSetting.is_active.is_(True))).all()
    for setting in existing_settings:
        setting.is_active = False

    session.query(SoldPlayer).delete(synchronize_session=False)
    session.query(TeamRoster).delete(synchronize_session=False)
    session.query(AuctionEvent).delete(synchronize_session=False)
    session.query(Captain).delete(synchronize_session=False)
    session.query(Team).delete(synchronize_session=False)
    session.flush()

    new_setting = AuctionSetting(
        tournament_name=payload.tournament_name,
        number_of_teams=payload.number_of_teams,
        squad_size=payload.squad_size,
        total_points_per_captain=Decimal(str(payload.total_points_per_captain)),
        captain_self_value_deduction=Decimal(str(payload.captain_self_value_deduction)),
        max_bid=Decimal(str(payload.max_bid)),
        is_active=True,
    )
    session.add(new_setting)
    session.flush()

    for team_payload in payload.teams:
        team = Team(
            auction_setting_id=new_setting.id,
            name=team_payload.team_name,
            owner_name=team_payload.owner_name,
            starting_budget=Decimal(str(payload.total_points_per_captain)),
            remaining_budget=Decimal(str(payload.total_points_per_captain - payload.captain_self_value_deduction)),
            max_bid_limit=Decimal(str(payload.max_bid)),
            squad_size_target=payload.squad_size,
            is_my_team=team_payload.is_my_team,
        )
        session.add(team)
        session.flush()

        captain = Captain(
            team_id=team.id,
            player_id=team_payload.captain_player_id,
            captain_name=team_payload.captain_name,
            self_cost_deduction=Decimal(str(payload.captain_self_value_deduction)),
        )
        session.add(captain)
        session.flush()

        if team_payload.captain_player_id is not None:
            session.add(
                TeamRoster(
                    team_id=team.id,
                    player_id=team_payload.captain_player_id,
                    purchase_price=Decimal(str(payload.captain_self_value_deduction)),
                    status=RosterStatus.CAPTAIN_RETAINED,
                )
            )

    sync_captain_pool_entries(session)
    session.commit()
    return get_auction_setup(session)


def get_or_create_player(session: Session, player_name: str) -> tuple[Player, bool]:
    player = session.scalar(select(Player).where(Player.name == player_name))
    if player is not None:
        return player, False

    player = Player(name=player_name, display_name=player_name)
    session.add(player)
    session.flush()
    return player, True


def sync_captain_pool_entries(session: Session) -> None:
    captain_player_ids = {
        player_id
        for player_id in session.scalars(select(Captain.player_id)).all()
        if player_id is not None
    }

    pool_entries = session.scalars(select(CurrentPlayerPool)).all()
    for entry in pool_entries:
        if entry.player_id in captain_player_ids:
            entry.status = PoolStatus.WITHDRAWN
            entry.is_captain = True
        elif entry.status == PoolStatus.WITHDRAWN:
            entry.status = PoolStatus.AVAILABLE


def upload_current_player_pool(
    session: Session,
    source_file: str,
    file_bytes: bytes,
) -> dict:
    parsed_rows, mapped_columns, missing_columns = parse_current_player_pool_excel(file_bytes)
    if missing_columns:
        return {
            "source_file": source_file,
            "rows_read": 0,
            "rows_saved": 0,
            "players_created": 0,
            "captains_marked": 0,
            "mapped_columns": mapped_columns,
            "missing_columns": missing_columns,
        }

    session.query(CurrentPlayerPool).delete()
    session.flush()

    rows_saved = 0
    players_created = 0
    captains_marked = 0
    seen_players: set[str] = set()

    for row in parsed_rows:
        player_name = normalize_player_name(row["player_name"])
        if not player_name:
            continue
        if player_name in seen_players:
            continue
        seen_players.add(player_name)

        player, was_created = get_or_create_player(session, player_name)
        if was_created:
            players_created += 1

        pool_entry = CurrentPlayerPool(
            player_id=player.id,
            source_file=source_file,
            status=PoolStatus.AVAILABLE,
            auction_order=row.get("auction_order"),
            is_captain=row.get("is_captain", False),
            reserve_price=Decimal(str(row.get("reserve_price", 0))) if row.get("reserve_price") is not None else None,
        )
        session.add(pool_entry)
        rows_saved += 1
        if pool_entry.is_captain:
            captains_marked += 1

    sync_captain_pool_entries(session)
    session.commit()

    return {
        "source_file": source_file,
        "rows_read": len(parsed_rows),
        "rows_saved": rows_saved,
        "players_created": players_created,
        "captains_marked": captains_marked,
        "mapped_columns": mapped_columns,
        "missing_columns": missing_columns,
    }


def get_current_player_pool_status(session: Session) -> dict:
    entries = session.scalars(select(CurrentPlayerPool)).all()
    return {
        "rows_loaded": len(entries),
        "captains_loaded": sum(1 for entry in entries if entry.is_captain),
    }
