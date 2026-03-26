from __future__ import annotations

from io import BytesIO
import re
from typing import Any

import pandas as pd

from app.core.column_mappings import COLUMN_MAPPINGS, REQUIRED_FIELDS

SUPPORTED_DATASETS = {"batting", "bowling", "fielding", "current_player_pool"}
HEADER_SCAN_LIMIT = 10


def normalize_column_name(name: str) -> str:
    normalized = str(name).strip().lower()
    normalized = normalized.replace("\u00a0", " ")
    normalized = normalized.replace("Â", "")
    normalized = re.sub(r"[^a-z0-9.]+", "", normalized)
    return normalized


def normalize_player_name(name: Any) -> str | None:
    if pd.isna(name):
        return None

    cleaned = " ".join(str(name).strip().split())
    return cleaned or None


def to_int(value: Any) -> int:
    if pd.isna(value):
        return 0

    cleaned = str(value).strip()
    if cleaned in {"", "-", "--", "na", "n/a", "none"}:
        return 0

    return int(float(cleaned))


def to_float(value: Any) -> float:
    if pd.isna(value):
        return 0.0

    cleaned = str(value).strip()
    if cleaned in {"", "-", "--", "na", "n/a", "none"}:
        return 0.0

    return float(cleaned)


def read_excel_without_header(file_bytes: bytes) -> pd.DataFrame:
    return pd.read_excel(BytesIO(file_bytes), header=None)


def build_column_lookup(dataframe: pd.DataFrame) -> dict[str, str]:
    return {normalize_column_name(column): str(column) for column in dataframe.columns}


def resolve_mapped_columns(dataset_type: str, dataframe: pd.DataFrame) -> tuple[dict[str, str], list[str]]:
    column_lookup = build_column_lookup(dataframe)
    mappings = {**COLUMN_MAPPINGS["shared"], **COLUMN_MAPPINGS[dataset_type]}

    resolved: dict[str, str] = {}
    missing: list[str] = []

    for standard_field, aliases in mappings.items():
        normalized_aliases = [normalize_column_name(alias) for alias in aliases]
        matched_column = next(
            (column_lookup[alias] for alias in normalized_aliases if alias in column_lookup),
            None,
        )
        if matched_column is None:
            if standard_field in REQUIRED_FIELDS[dataset_type]:
                missing.append(standard_field)
            continue
        resolved[standard_field] = matched_column

    return resolved, missing


def score_header_row(dataset_type: str, row_values: list[Any]) -> int:
    mappings = {**COLUMN_MAPPINGS["shared"], **COLUMN_MAPPINGS[dataset_type]}
    normalized_cells = {normalize_column_name(value) for value in row_values if not pd.isna(value)}

    score = 0
    for aliases in mappings.values():
        normalized_aliases = [normalize_column_name(alias) for alias in aliases]
        if any(alias in normalized_cells for alias in normalized_aliases):
            score += 1
    return score


def detect_header_row(dataset_type: str, file_bytes: bytes) -> int:
    raw_dataframe = read_excel_without_header(file_bytes)
    best_row_index = 0
    best_score = -1

    for row_index in range(min(len(raw_dataframe.index), HEADER_SCAN_LIMIT)):
        row_values = raw_dataframe.iloc[row_index].tolist()
        row_score = score_header_row(dataset_type, row_values)
        if row_score > best_score:
            best_score = row_score
            best_row_index = row_index

    return best_row_index


def parse_historical_excel(dataset_type: str, file_bytes: bytes) -> tuple[list[dict[str, Any]], dict[str, str], list[str]]:
    if dataset_type not in SUPPORTED_DATASETS:
        raise ValueError(f"Unsupported dataset_type '{dataset_type}'.")

    header_row_index = detect_header_row(dataset_type, file_bytes)
    dataframe = pd.read_excel(BytesIO(file_bytes), header=header_row_index)
    mapped_columns, missing_columns = resolve_mapped_columns(dataset_type, dataframe)
    if missing_columns:
        return [], mapped_columns, missing_columns

    records: list[dict[str, Any]] = []
    for _, row in dataframe.iterrows():
        player_name = normalize_player_name(row[mapped_columns["player_name"]])
        if not player_name:
            continue

        base_record = {
            "player_name": player_name,
            "matches": to_int(row[mapped_columns["matches"]]),
        }

        if dataset_type == "batting":
            records.append(
                {
                    **base_record,
                    "innings": to_int(row[mapped_columns["innings"]]),
                    "runs": to_int(row.get(mapped_columns.get("runs"), 0)),
                    "average": to_float(row[mapped_columns["average"]]),
                    "strike_rate": to_float(row[mapped_columns["strike_rate"]]),
                    "fours": to_int(row[mapped_columns["fours"]]),
                }
            )
        elif dataset_type == "bowling":
            records.append(
                {
                    **base_record,
                    "overs": to_float(row[mapped_columns["overs"]]),
                    "wickets": to_int(row.get(mapped_columns.get("wickets"), 0)),
                    "average": to_float(row[mapped_columns["average"]]),
                    "economy": to_float(row[mapped_columns["economy"]]),
                }
            )
        else:
            records.append(
                {
                    **base_record,
                    "catches": to_int(row[mapped_columns["catches"]]),
                    "direct_run_outs": to_int(row[mapped_columns["direct_run_outs"]]),
                    "indirect_run_outs": to_int(row[mapped_columns["indirect_run_outs"]]),
                }
            )

    return records, mapped_columns, missing_columns


def parse_boolean(value: Any) -> bool:
    if pd.isna(value):
        return False

    cleaned = str(value).strip().lower()
    return cleaned in {"1", "true", "yes", "y", "captain"}


def parse_current_player_pool_excel(file_bytes: bytes) -> tuple[list[dict[str, Any]], dict[str, str], list[str]]:
    dataset_type = "current_player_pool"
    header_row_index = detect_header_row(dataset_type, file_bytes)
    dataframe = pd.read_excel(BytesIO(file_bytes), header=header_row_index)
    mapped_columns, missing_columns = resolve_mapped_columns(dataset_type, dataframe)
    if missing_columns:
        return [], mapped_columns, missing_columns

    records: list[dict[str, Any]] = []
    for _, row in dataframe.iterrows():
        player_name = normalize_player_name(row[mapped_columns["player_name"]])
        if not player_name:
            continue

        records.append(
            {
                "player_name": player_name,
                "is_captain": parse_boolean(row.get(mapped_columns.get("is_captain"), False)),
                "reserve_price": (
                    to_float(row.get(mapped_columns["reserve_price"]))
                    if "reserve_price" in mapped_columns
                    else None
                ),
                "auction_order": (
                    to_int(row.get(mapped_columns["auction_order"]))
                    if "auction_order" in mapped_columns
                    else None
                ),
            }
        )

    return records, mapped_columns, missing_columns
