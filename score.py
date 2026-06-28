# أوزان التقييم

WEIGHTS = {
    "vwap": 20,
    "volume": 20,
    "rvol": 15,
    "atr": 15,
    "trend": 15,
    "breakout": 15
}


def calculate_score(checks):
    score = 0

    for key, passed in checks.items():
        if passed and key in WEIGHTS:
            score += WEIGHTS[key]

    return score
