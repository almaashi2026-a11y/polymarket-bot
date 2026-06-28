import yfinance as yf

MIN_PRICE = 0.2
MAX_PRICE = 10


def get_rvol(data):
    avg = data["Volume"].rolling(20).mean().iloc[-1]
    last = data["Volume"].iloc[-1]
    return last / avg if avg else 0


def scan_symbol(symbol):
    data = yf.download(symbol, period="1mo", interval="1d", progress=False)

    if data.empty or len(data) < 10:
        return None

    price = float(data["Close"].iloc[-1])
    prev = float(data["Close"].iloc[-2])

    change = ((price - prev) / prev) * 100
    rvol = get_rvol(data)

    if not (MIN_PRICE <= price <= MAX_PRICE):
        return None

    if rvol < 2:
        return None

    if change < 2:
        return None

    return {
        "symbol": symbol,
        "price": round(price, 2),
        "change": round(change, 2),
        "rvol": round(rvol, 2)
    }


def scan_market(symbols):
    results = []

    for s in symbols:
        res = scan_symbol(s)
        if res:
            results.append(res)

    return results
