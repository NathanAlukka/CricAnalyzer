from app.core.scoring_config import BID_RECOMMENDATION_CONFIG


def test_bid_recommendation_config_values_exist():
    assert BID_RECOMMENDATION_CONFIG["good_buy_discount"] < 1
    assert BID_RECOMMENDATION_CONFIG["hard_cap_markup"] > 1
    assert BID_RECOMMENDATION_CONFIG["score_bonus_multiplier"] > 0
    assert BID_RECOMMENDATION_CONFIG["target_bowlers"] == 7
