"""Editable column aliases for uploaded Excel files.

If your source files use different column names, update the values here
instead of changing parsing logic in multiple places.
"""

COLUMN_MAPPINGS = {
    "shared": {
        "player_name": ["player", "player name", "name", "player_name"],
        "matches": ["matches", "mat", "m", "match played", "matches played"],
    },
    "batting": {
        "innings": ["inns", "innings", "inn"],
        "runs": ["runs", "r"],
        "average": ["average", "avg", "bat avg", "batting average"],
        "strike_rate": ["strike rate", "sr", "strike_rate"],
        "fours": ["4s", "4's", "fours", "4", "boundaries"],
    },
    "bowling": {
        "overs": ["overs", "over", "ovs"],
        "wickets": ["wickets", "wkts", "wkt"],
        "average": ["average", "avg", "bowl avg", "bowling average"],
        "economy": ["economy", "econ", "economy rate"],
    },
    "fielding": {
        "catches": ["catches", "ct", "catch"],
        "direct_run_outs": ["direct run outs", "direct ro", "direct runout", "dro"],
        "indirect_run_outs": ["indirect run outs", "indirect ro", "indirect runout", "indirectro", "iro"],
    },
    "current_player_pool": {
        "player_name": ["player", "player name", "name", "player_name"],
        "is_captain": ["captain", "is captain", "captain?", "is_captain"],
        "reserve_price": ["reserve price", "reserve", "base price", "reserve_price"],
        "auction_order": ["auction order", "order", "nomination order", "auction_order"],
    },
}

REQUIRED_FIELDS = {
    "batting": ["player_name", "matches", "innings", "average", "strike_rate", "fours"],
    "bowling": ["player_name", "matches", "overs", "average", "economy"],
    "fielding": ["player_name", "matches", "catches", "direct_run_outs", "indirect_run_outs"],
    "current_player_pool": ["player_name"],
}
