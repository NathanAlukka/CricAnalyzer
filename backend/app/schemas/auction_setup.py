from pydantic import BaseModel, Field


class CaptainSetupItem(BaseModel):
    team_name: str = Field(min_length=1, max_length=120)
    owner_name: str | None = Field(default=None, max_length=120)
    captain_name: str = Field(min_length=1, max_length=120)
    captain_player_id: int | None = None
    is_my_team: bool = False


class AuctionSettingsSaveRequest(BaseModel):
    tournament_name: str = Field(min_length=1, max_length=120)
    number_of_teams: int = Field(ge=2, le=20)
    squad_size: int = Field(ge=1, le=30)
    total_points_per_captain: float = Field(ge=0)
    captain_self_value_deduction: float = Field(ge=0)
    max_bid: float = Field(ge=0)
    teams: list[CaptainSetupItem]


class CaptainSetupResponse(BaseModel):
    team_name: str
    owner_name: str | None
    captain_name: str
    captain_player_id: int | None
    is_my_team: bool


class AuctionSettingsResponse(BaseModel):
    tournament_name: str
    number_of_teams: int
    squad_size: int
    total_points_per_captain: float
    captain_self_value_deduction: float
    max_bid: float
    teams: list[CaptainSetupResponse]


class PlayerOptionItem(BaseModel):
    id: int
    name: str


class PlayerOptionListResponse(BaseModel):
    items: list[PlayerOptionItem]


class CurrentPlayerPoolUploadResult(BaseModel):
    source_file: str
    rows_read: int
    rows_saved: int
    players_created: int
    captains_marked: int
    mapped_columns: dict[str, str]
    missing_columns: list[str]


class CurrentPlayerPoolStatusResponse(BaseModel):
    rows_loaded: int
    captains_loaded: int
