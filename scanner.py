import requests
from config import FINNHUB_API_KEY

BASE_URL = "https://finnhub.io/api/v1"

def get_stock_price(symbol):

    url = f"{BASE_URL}/quote?symbol={symbol}&token={FINNHUB_API_KEY}"

    response = requests.get(url)
    data = response.json()

    return {
        "symbol": symbol,
        "price": data["c"],
        "high": data["h"],
        "low": data["l"],
        "open": data["o"],
        "previous_close": data["pc"]
    }
