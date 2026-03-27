from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.post_auction import PostAuctionAnalysisResponse
from app.services.post_auction_analysis_service import get_post_auction_analysis

router = APIRouter(prefix="/post-auction-analysis", tags=["post-auction-analysis"])


@router.get("", response_model=PostAuctionAnalysisResponse)
def read_post_auction_analysis(
    session: Session = Depends(get_db_session),
) -> PostAuctionAnalysisResponse:
    return PostAuctionAnalysisResponse(**get_post_auction_analysis(session))
