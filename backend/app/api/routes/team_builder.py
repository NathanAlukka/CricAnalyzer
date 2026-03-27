from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.team_builder import TeamBuilderResponse
from app.services.team_builder_service import get_team_builder_data

router = APIRouter(prefix="/team-builder", tags=["team-builder"])


@router.get("", response_model=TeamBuilderResponse)
def read_team_builder(session: Session = Depends(get_db_session)) -> TeamBuilderResponse:
    return TeamBuilderResponse(**get_team_builder_data(session))
