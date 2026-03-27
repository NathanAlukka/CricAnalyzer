from pydantic import BaseModel, Field


class LiveAuctionPlayerItem(BaseModel):
    player_id: int
    player_name: str
    team_name: str | None
    role_hint: str
    batting_score: float
    bowling_score: float
    fielding_score: float
    overall_score: float
    is_captain: bool
    reserve_price: float | None
    auction_order: int | None


class LiveAuctionTeamItem(BaseModel):
    team_id: int
    team_name: str
    owner_name: str | None
    remaining_budget: float
    squad_size_target: int | None
    players_bought: int
    is_my_team: bool


class LiveAuctionEventItem(BaseModel):
    event_id: int
    player_name: str
    team_name: str | None
    event_type: str
    final_price: float | None
    nomination_order: int | None


class MyTeamSummary(BaseModel):
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


class LiveAuctionStateResponse(BaseModel):
    remaining_pool: list[LiveAuctionPlayerItem]
    teams: list[LiveAuctionTeamItem]
    my_team_summary: MyTeamSummary | None
    recent_events: list[LiveAuctionEventItem]


class SubmitAuctionEventRequest(BaseModel):
    player_id: int
    event_type: str = Field(pattern="^(bought_by_me|bought_by_other|unsold)$")
    team_id: int | None = None
    final_price: float | None = Field(default=None, ge=0)
    notes: str | None = None


class SubmitAuctionEventResponse(BaseModel):
    message: str


class ResetAuctionResponse(BaseModel):
    message: str


class BidRecommendationResponse(BaseModel):
    player_id: int
    player_name: str
    fair_value: float
    good_buy_upto: float
    overpay_threshold: float
    hard_cap: float
    recommendation_label: str
    recommendation_reason: str
    scarcity_score: float
    team_need_score: float
