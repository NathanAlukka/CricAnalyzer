from pydantic import BaseModel


class UploadResultResponse(BaseModel):
    dataset_type: str
    source_file: str
    rows_read: int
    rows_saved: int
    players_created: int
    mapped_columns: dict[str, str]
    missing_columns: list[str]


class DatasetStatusItem(BaseModel):
    dataset_type: str
    rows_loaded: int
    loaded: bool


class HistoricalDataStatusResponse(BaseModel):
    items: list[DatasetStatusItem]
