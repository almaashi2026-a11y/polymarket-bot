from symbols import SYMBOLS
from market import get_quote
from score import calculate_score


def scan_market():

    results = []

    for symbol in SYMBOLS:

        stock = get_quote(symbol)

        if not stock:
            continue

        checks = {

            "vwap": stock["change_percent"] > 2,

            "volume": stock["price"] > 1,

            "rvol": stock["change_percent"] > 1,

            "atr": stock["high"] > stock["low"],

            "trend": stock["price"] > stock["previous_close"],

            "breakout": stock["change_percent"] > 3

        }

        score = calculate_score(checks)

        stock["score"] = score

        results.append(stock)

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
