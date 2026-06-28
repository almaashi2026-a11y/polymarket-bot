"""
المرحلة الأولى (Stage 1): فلترة سريعة عبر Finnhub.
يفحص كل رموز NASDAQ (آلاف الرموز) بسرعة باستخدام endpoint خفيف (quote فقط)،
ويرجع فقط الرموز اللي يحتمل عليها زخم — عشان المرحلة الثانية (yfinance)
ما تحتاج تحسب EMA9/VWAP الثقيلة إلا على عدد صغير من المرشحين.

نستخدم ThreadPoolExecutor لتسريع آلاف الطلبات (Finnhub يدعم هذا بسهولة
لأن quote endpoint خفيف جداً مقارنة بـ candles).
"""

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from config import (
    FINNHUB_API_KEY,
    MIN_PRICE,
    MAX_PRICE,
    STAGE1_MIN_CHANGE_PERCENT,
    STAGE1_MAX_WORKERS,
)

BASE_URL = "https://finnhub.io/api/v1"


def _quick_quote(symbol):
    """يجيب فقط السعر والتغير اليومي — endpoint خفيف وسريع."""
    url = f"{BASE_URL}/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if not data or "c" not in data or data["c"] in (0, None):
            return None

        price = data["c"]
        change_percent = data.get("dp", 0) or 0

        # فلتر السعر (Penny Stocks)
        if price < MIN_PRICE or price > MAX_PRICE:
            return None

        # فلتر تغير أولي تقريبي — نقبل تحرك إيجابي أو سلبي بقوة (نهتم بالإيجابي أكثر)
        if abs(change_percent) < STAGE1_MIN_CHANGE_PERCENT:
            return None

        return {
            "symbol": symbol,
            "price": price,
            "change_percent": change_percent,
        }

    except Exception:
        return None


def get_candidates(symbols):
    """
    يفحص قائمة الرموز بالتوازي (threads) ويرجع فقط الرموز اللي عدت
    فلتر السعر + فلتر التغير الأولي. هذي القائمة المختصرة تروح للمرحلة
    الثانية (yfinance) لحساب EMA9/VWAP/RVOL بدقة.
    """
    candidates = []

    with ThreadPoolExecutor(max_workers=STAGE1_MAX_WORKERS) as executor:
        futures = {executor.submit(_quick_quote, symbol): symbol for symbol in symbols}

        for future in as_completed(futures):
            result = future.result()
            if result:
                candidates.append(result["symbol"])

    return candidates
