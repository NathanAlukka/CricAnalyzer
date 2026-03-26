from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.auction_setup import (
    AuctionSettingsResponse,
    AuctionSettingsSaveRequest,
    CurrentPlayerPoolStatusResponse,
    CurrentPlayerPoolUploadResult,
    PlayerOptionListResponse,
)
from app.services.auction_setup_service import (
    get_auction_setup,
    get_current_player_pool_status,
    get_player_options,
    save_auction_setup,
    upload_current_player_pool,
)

router = APIRouter(prefix="/auction-setup", tags=["auction-setup"])


@router.get("", response_model=AuctionSettingsResponse)
def read_auction_setup(session: Session = Depends(get_db_session)) -> AuctionSettingsResponse:
    return AuctionSettingsResponse(**get_auction_setup(session))


@router.post("/settings", response_model=AuctionSettingsResponse)
def create_or_update_auction_setup(
    payload: AuctionSettingsSaveRequest,
    session: Session = Depends(get_db_session),
) -> AuctionSettingsResponse:
    return AuctionSettingsResponse(**save_auction_setup(session, payload))


@router.get("/player-options", response_model=PlayerOptionListResponse)
def read_player_options(session: Session = Depends(get_db_session)) -> PlayerOptionListResponse:
    return PlayerOptionListResponse(items=get_player_options(session))


@router.get("/player-pool/status", response_model=CurrentPlayerPoolStatusResponse)
def read_current_player_pool_status(
    session: Session = Depends(get_db_session),
) -> CurrentPlayerPoolStatusResponse:
    return CurrentPlayerPoolStatusResponse(**get_current_player_pool_status(session))


@router.post("/player-pool/upload", response_model=CurrentPlayerPoolUploadResult)
async def upload_current_player_pool_file(
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
) -> CurrentPlayerPoolUploadResult:
    file_bytes = await file.read()
    result = upload_current_player_pool(session, file.filename, file_bytes)
    return CurrentPlayerPoolUploadResult(**result)
