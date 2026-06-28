from symbols import SYMBOLS
from market_finnhub import get_candidates
from market import get_quote
from score import calculate_score, passes_entry_filter
from alerts import filter_new_alerts


def scan_market():
    candidates = get_candidates(SYMBOLS)
    print(f"🔎 Stage 1 (Finnhub): {len(candidates)} مرشح من أصل {len(SYMBOLS)} رمز")

    qualified = []

    for symbol in candidates:
        stock = get_quote(symbol)
        if not stock:
            continue

        if not passes_entry_filter(stock):
            continue

        stock["score"] = calculate_score(stock)
        qualified.append(stock)

    qualified.sort(key=lambda x: x["score"], reverse=True)

    new_alerts = filter_new_alerts(qualified)

    return qualified, new_alerts
