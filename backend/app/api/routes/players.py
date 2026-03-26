from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.player_database import PlayerDatabaseResponse
from app.schemas.player_detail import PlayerDetailResponse
from app.services.player_database_service import get_player_database
from app.services.player_detail_service import get_player_detail

router = APIRouter(prefix="/players", tags=["players"])


@router.get("", response_model=PlayerDatabaseResponse)
def list_players(
    search: str | None = Query(default=None),
    role_hint: str | None = Query(default=None),
    session: Session = Depends(get_db_session),
) -> PlayerDatabaseResponse:
    items = get_player_database(session, search=search, role_hint=role_hint)
    return PlayerDatabaseResponse(items=items)


@router.get("/{player_id}", response_model=PlayerDetailResponse)
def get_player(player_id: int, session: Session = Depends(get_db_session)) -> PlayerDetailResponse:
    item = get_player_detail(session, player_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Player not found.")
    return PlayerDetailResponse(**item)
