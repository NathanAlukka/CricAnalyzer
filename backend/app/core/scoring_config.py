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
    "batter_min": 3.7,
    "bowler_min": 5.0,
    "fielding_asset_min": 4.0,
}

MINIMUM_SAMPLE_LIMITS = {
    "batting_innings_max_zero_score": 7,
    "bowling_overs_max_zero_score": 7.0,
}

SCORING_VERSION = "v1"
SCORE_SCALE_MAX = 10.0

BID_RECOMMENDATION_CONFIG = {
    "good_buy_discount": 0.88,
    "overpay_markup": 1.22,
    "hard_cap_markup": 1.45,
    "budget_safety_ratio": 1.0,
    "score_bonus_multiplier": 2.0,
    "priority_target_min": 20.0,
    "good_value_min": 13.0,
    "skip_max": 6.5,
    "target_bowlers": 7,
    "target_batting_ratio": 0.75,
}
