import requests
from config import FINNHUB_API_KEY

BASE_URL = "https://finnhub.io/api/v1"

def get_quote(symbol):
    url = f"{BASE_URL}/quote?symbol={symbol}&token={FINNHUB_API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data and "c" in data:
            return {
                "symbol": symbol,
                "price": data["c"],
                "change": data["d"],
                "change_percent": data["dp"],
                "high": data["h"],
                "low": data["l"],
                "open": data["o"],
                "previous_close": data["pc"]
            }

    except Exception as e:
        print(f"Market Error: {e}")

    return None
