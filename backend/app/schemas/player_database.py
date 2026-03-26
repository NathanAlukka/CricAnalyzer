from pydantic import BaseModel


class PlayerDatabaseItem(BaseModel):
    id: int
    name: str
    team_name: str | None
    role_hint: str
    batting_score: float
    bowling_score: float
    fielding_score: float
    overall_score: float


class PlayerDatabaseResponse(BaseModel):
    items: list[PlayerDatabaseItem]
