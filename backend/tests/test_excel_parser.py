from io import BytesIO

import pandas as pd

from app.services.excel_parser import parse_historical_excel


def test_parse_batting_excel_maps_common_columns() -> None:
    dataframe = pd.DataFrame(
        {
            "Player Name": ["Virat Kohli", "AB de Villiers"],
            "Mat": [10, 8],
            "Inns": [10, 8],
            "Avg": [45.5, 39.0],
            "SR": [140.2, 151.6],
            "4s": [20, 15],
            "Runs": [455, 312],
        }
    )

    buffer = BytesIO()
    dataframe.to_excel(buffer, index=False)
    excel_bytes = buffer.getvalue()

    records, mapped_columns, missing_columns = parse_historical_excel("batting", excel_bytes)

    assert missing_columns == []
    assert mapped_columns["player_name"] == "Player Name"
    assert records[0]["player_name"] == "Virat Kohli"
    assert records[0]["matches"] == 10
    assert records[0]["innings"] == 10
    assert records[0]["fours"] == 20


def test_parse_batting_excel_detects_header_after_title_rows() -> None:
    dataframe = pd.DataFrame(
        [
            ["Willows Premier League Batting", None, None, None, None, None],
            ["Season Summary", None, None, None, None, None],
            ["Player", "Mat", "Inns", "Avg", "SR", "4s"],
            ["Virat Kohli", 10, 10, 45.5, 140.2, 20],
            ["AB de Villiers", 8, 8, 39.0, 151.6, 15],
        ]
    )

    buffer = BytesIO()
    dataframe.to_excel(buffer, index=False, header=False)
    excel_bytes = buffer.getvalue()

    records, mapped_columns, missing_columns = parse_historical_excel("batting", excel_bytes)

    assert missing_columns == []
    assert mapped_columns["player_name"] == "Player"
    assert records[0]["player_name"] == "Virat Kohli"
    assert records[0]["matches"] == 10
    assert records[0]["innings"] == 10


def test_parse_batting_excel_handles_formatted_header_labels() -> None:
    dataframe = pd.DataFrame(
        [
            ["All Series Batting Records - Willows Premier League", None, None, None, None, None],
            ["Player\u00a0", "Mat\u00a0", "Inns\u00a0", "Avg\u00a0", "SR\u00a0", "4's\u00a0"],
            ["Virat Kohli", 10, 10, 45.5, 140.2, 20],
        ]
    )

    buffer = BytesIO()
    dataframe.to_excel(buffer, index=False, header=False)
    excel_bytes = buffer.getvalue()

    records, mapped_columns, missing_columns = parse_historical_excel("batting", excel_bytes)

    assert missing_columns == []
    assert mapped_columns["fours"] == "4's\u00a0"
    assert mapped_columns["innings"] == "Inns\u00a0"
    assert records[0]["fours"] == 20


def test_parse_batting_excel_treats_dash_placeholders_as_zero() -> None:
    dataframe = pd.DataFrame(
        [
            ["Player", "Mat", "Inns", "Avg", "SR", "4s"],
            ["Nathan Alukka", 5, 5, "--", 120.0, 4],
        ]
    )

    buffer = BytesIO()
    dataframe.to_excel(buffer, index=False, header=False)
    excel_bytes = buffer.getvalue()

    records, _, missing_columns = parse_historical_excel("batting", excel_bytes)

    assert missing_columns == []
    assert records[0]["innings"] == 5
    assert records[0]["average"] == 0.0
