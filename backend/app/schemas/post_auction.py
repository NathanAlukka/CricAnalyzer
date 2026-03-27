from pydantic import BaseModel


class PostAuctionTeamTopPlayer(BaseModel):
    player_name: str
    overall_score: float


class PostAuctionTeamItem(BaseModel):
    team_id: int
    team_name: str
    owner_name: str | None
    players_count: int
    remaining_budget: float
    batting_total: float
    bowling_total: float
    fielding_total: float
    overall_total: float
    batter_count: int
    bowler_count: int
    all_rounder_count: int
    fielding_asset_count: int
    strengths: list[str]
    weaknesses: list[str]
    top_players: list[PostAuctionTeamTopPlayer]


class BestValueBuyItem(BaseModel):
    player_name: str
    team_name: str
    sold_price: float
    overall_score: float
    value_index: float


class PostAuctionAnalysisResponse(BaseModel):
    teams: list[PostAuctionTeamItem]
    contender_team_names: list[str]
    average_team_overall: float
    best_value_buys: list[BestValueBuyItem]
