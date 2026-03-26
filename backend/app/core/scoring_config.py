"""Editable scoring weights and thresholds.

This file is the main place to change how batting, bowling,
fielding, and overall scores are calculated.
"""

SCORING_WEIGHTS = {
    "batting": {
        "fours": 0.20,
        "strike_rate": 0.40,
        "average": 0.40,
    },
    "bowling": {
        "economy": 0.66,
        "average": 0.34,
    },
    "fielding": {
        "catches_per_match": 0.45,
        "direct_run_outs_per_match": 0.45,
        "indirect_run_outs_per_match": 0.10,
    },
    "overall": {
        "batting": 0.40,
        "bowling": 0.40,
        "fielding": 0.20,
    },
}

ROLE_HINT_THRESHOLDS = {
    "all_rounder_min": 6.0,
    "fielding_asset_min": 7.0,
    "specialist_gap": 1.0,
}

MINIMUM_SAMPLE_LIMITS = {
    "batting_innings_max_zero_score": 7,
    "bowling_overs_max_zero_score": 7.0,
}

SCORING_VERSION = "v1"
SCORE_SCALE_MAX = 10.0
