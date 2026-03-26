from pydantic import BaseModel


class PlayerStatSummary(BaseModel):
    matches: int
    runs: int | None = None
    average: float | None = None
    strike_rate: float | None = None
    fours: int | None = None
    wickets: int | None = None
    economy: float | None = None
    catches: int | None = None
    direct_run_outs: int | None = None
    indirect_run_outs: int | None = None


class PlayerAverageComparison(BaseModel):
    batting_score: float
    bowling_score: float
    fielding_score: float
    overall_score: float


class PlayerDetailResponse(BaseModel):
    id: int
    name: str
    team_name: str | None
    role_hint: str
    batting_score: float
    bowling_score: float
    fielding_score: float
    overall_score: float
    batting_stats: PlayerStatSummary | None
    bowling_stats: PlayerStatSummary | None
    fielding_stats: PlayerStatSummary | None
    batting_average_stats: PlayerStatSummary | None
    bowling_average_stats: PlayerStatSummary | None
    fielding_average_stats: PlayerStatSummary | None
    player_scores: PlayerAverageComparison
    average_scores: PlayerAverageComparison
