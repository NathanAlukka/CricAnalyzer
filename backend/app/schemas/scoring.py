from pydantic import BaseModel


class ScoreProcessingResponse(BaseModel):
    players_processed: int
    scores_created: int
    scoring_version: str
