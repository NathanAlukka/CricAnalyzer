from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.scoring import ScoreProcessingResponse
from app.services.scoring_service import process_player_scores

router = APIRouter(prefix="/scoring", tags=["scoring"])


@router.post("/process", response_model=ScoreProcessingResponse)
def process_scores(session: Session = Depends(get_db_session)) -> ScoreProcessingResponse:
    return ScoreProcessingResponse(**process_player_scores(session))
