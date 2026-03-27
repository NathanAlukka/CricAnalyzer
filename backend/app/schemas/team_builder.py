from pydantic import BaseModel


class TeamBuilderRosterItem(BaseModel):
    player_id: int
    player_name: str
    role_hint: str
    roster_status: str
    purchase_price: float | None
    batting_score: float
    bowling_score: float
    fielding_score: float
    overall_score: float


class TeamBuilderSummary(BaseModel):
    team_name: str
    remaining_budget: float
    squad_size_target: int | None
    players_bought: int
    open_slots: int
    batter_count: int
    bowler_count: int
    all_rounder_count: int
    fielding_asset_count: int
    batting_total: float
    bowling_total: float
    fielding_total: float
    overall_total: float


class TeamBuilderResponse(BaseModel):
    summary: TeamBuilderSummary | None
    roster: list[TeamBuilderRosterItem]
