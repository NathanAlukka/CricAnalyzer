from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.live_auction import (
    LiveAuctionStateResponse,
    ResetAuctionResponse,
    SubmitAuctionEventRequest,
    SubmitAuctionEventResponse,
)
from app.services.live_auction_service import (
    get_live_auction_state,
    reset_live_auction,
    submit_live_auction_event,
)

router = APIRouter(prefix="/live-auction", tags=["live-auction"])


@router.get("/state", response_model=LiveAuctionStateResponse)
def read_live_auction_state(session: Session = Depends(get_db_session)) -> LiveAuctionStateResponse:
    return LiveAuctionStateResponse(**get_live_auction_state(session))


@router.post("/reset", response_model=ResetAuctionResponse)
def reset_auction(session: Session = Depends(get_db_session)) -> ResetAuctionResponse:
    return ResetAuctionResponse(**reset_live_auction(session))


@router.post("/events", response_model=SubmitAuctionEventResponse)
def create_auction_event(
    payload: SubmitAuctionEventRequest,
    session: Session = Depends(get_db_session),
) -> SubmitAuctionEventResponse:
    try:
        return SubmitAuctionEventResponse(**submit_live_auction_event(session, payload))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
