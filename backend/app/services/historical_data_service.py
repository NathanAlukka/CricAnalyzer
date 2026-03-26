from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import BattingStat, BowlingStat, FieldingStat, Player
from app.services.excel_parser import parse_historical_excel


DATASET_MODEL_MAP = {
    "batting": BattingStat,
    "bowling": BowlingStat,
    "fielding": FieldingStat,
}


def score_record_quality(dataset_type: str, row: dict) -> tuple:
    """Rank duplicate rows so the importer keeps the most useful one."""

    if dataset_type == "batting":
        return (row["matches"], row["innings"], row["runs"], row["average"], row["strike_rate"], row["fours"])
    if dataset_type == "bowling":
        return (row["matches"], row["overs"], row["wickets"], row["average"], row["economy"])
    return (
        row["matches"],
        row["catches"],
        row["direct_run_outs"],
        row["indirect_run_outs"],
    )


def deduplicate_rows(dataset_type: str, parsed_rows: list[dict]) -> list[dict]:
    """Keep one row per player name for each uploaded file."""

    deduplicated: dict[str, dict] = {}
    for row in parsed_rows:
        existing = deduplicated.get(row["player_name"])
        if existing is None or score_record_quality(dataset_type, row) > score_record_quality(dataset_type, existing):
            deduplicated[row["player_name"]] = row

    return list(deduplicated.values())


def get_or_create_player(session: Session, player_name: str) -> tuple[Player, bool]:
    existing_player = session.scalar(select(Player).where(Player.name == player_name))
    if existing_player:
        return existing_player, False

    new_player = Player(name=player_name, display_name=player_name)
    session.add(new_player)
    session.flush()
    return new_player, True


def replace_dataset_rows(session: Session, dataset_model: type, source_file: str) -> None:
    session.query(dataset_model).filter(dataset_model.source_file == source_file).delete()


def save_historical_dataset(
    session: Session,
    dataset_type: str,
    source_file: str,
    file_bytes: bytes,
) -> dict:
    parsed_rows, mapped_columns, missing_columns = parse_historical_excel(dataset_type, file_bytes)
    if missing_columns:
        return {
            "dataset_type": dataset_type,
            "source_file": source_file,
            "rows_read": 0,
            "rows_saved": 0,
            "players_created": 0,
            "mapped_columns": mapped_columns,
            "missing_columns": missing_columns,
        }

    parsed_rows = deduplicate_rows(dataset_type, parsed_rows)
    dataset_model = DATASET_MODEL_MAP[dataset_type]
    replace_dataset_rows(session, dataset_model, source_file)

    rows_saved = 0
    players_created = 0

    for row in parsed_rows:
        player, was_created = get_or_create_player(session, row["player_name"])
        if was_created:
            players_created += 1

        if dataset_type == "batting":
            session.add(
                BattingStat(
                    player_id=player.id,
                    source_file=source_file,
                    matches=row["matches"],
                    innings=row["innings"],
                    runs=row["runs"],
                    average=row["average"],
                    strike_rate=row["strike_rate"],
                    fours=row["fours"],
                )
            )
        elif dataset_type == "bowling":
            session.add(
                BowlingStat(
                    player_id=player.id,
                    source_file=source_file,
                    matches=row["matches"],
                    overs=row["overs"],
                    wickets=row["wickets"],
                    average=row["average"],
                    economy=row["economy"],
                )
            )
        else:
            session.add(
                FieldingStat(
                    player_id=player.id,
                    source_file=source_file,
                    matches=row["matches"],
                    catches=row["catches"],
                    direct_run_outs=row["direct_run_outs"],
                    indirect_run_outs=row["indirect_run_outs"],
                )
            )

        rows_saved += 1

    session.commit()

    return {
        "dataset_type": dataset_type,
        "source_file": source_file,
        "rows_read": len(parsed_rows),
        "rows_saved": rows_saved,
        "players_created": players_created,
        "mapped_columns": mapped_columns,
        "missing_columns": missing_columns,
    }


def get_historical_data_status(session: Session) -> list[dict[str, int | str | bool]]:
    batting_count = session.scalar(select(func.count(BattingStat.id))) or 0
    bowling_count = session.scalar(select(func.count(BowlingStat.id))) or 0
    fielding_count = session.scalar(select(func.count(FieldingStat.id))) or 0

    return [
        {"dataset_type": "batting", "rows_loaded": batting_count, "loaded": batting_count > 0},
        {"dataset_type": "bowling", "rows_loaded": bowling_count, "loaded": bowling_count > 0},
        {"dataset_type": "fielding", "rows_loaded": fielding_count, "loaded": fielding_count > 0},
    ]
