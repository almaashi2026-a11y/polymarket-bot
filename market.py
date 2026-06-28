"""
يجلب بيانات الشموع الدقيقية (1-minute candles) من yfinance،
ويحسب: EMA9, VWAP, RVOL, التغير خلال آخر 15 دقيقة.

ملاحظة فنية: yfinance يعطي بيانات 1-minute فقط لآخر 7 أيام تداول،
وهذا كافٍ جداً لحساب اللحظي (intraday) اللي نحتاجه هنا.
"""

import pandas as pd
import yfinance as yf
from datetime import time as pd_time

from config import MIN_PRICE, MAX_PRICE, LOOKBACK_MINUTES


def _calculate_vwap(df):
    """VWAP = تراكمي(السعر النموذجي × الحجم) / تراكمي(الحجم) لليوم الحالي فقط."""
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    cumulative_vol = df["Volume"].cumsum()
    cumulative_pv = (typical_price * df["Volume"]).cumsum()
    vwap = cumulative_pv / cumulative_vol.replace(0, pd.NA)
    return vwap


def _calculate_rvol(df, current_volume_cumsum):
    """
    RVOL = حجم اليوم الحالي حتى هذه اللحظة / متوسط الحجم لنفس الفترة
    بالأيام السابقة المتاحة في نفس الجلب (تقريبي بسبب قيود yfinance المجانية).
    """
    if "day" not in df.columns:
        return 1.0

    days = df["day"].unique()
    if len(days) < 2:
        return 1.0  # لا يوجد تاريخ كافٍ للمقارنة، نرجع قيمة افتراضية محايدة

    today = days[-1]
    today_minutes_count = len(df[df["day"] == today])

    prior_days_volumes = []
    for d in days[:-1]:
        day_df = df[df["day"] == d].head(today_minutes_count)
        if len(day_df) > 0:
            prior_days_volumes.append(day_df["Volume"].sum())

    if not prior_days_volumes:
        return 1.0

    avg_prior_volume = sum(prior_days_volumes) / len(prior_days_volumes)
    if avg_prior_volume <= 0:
        return 1.0

    return current_volume_cumsum / avg_prior_volume


def _classify_session(timestamp):
    """
    يصنف الجلسة بناءً على توقيت نيويورك (EST/EDT):
    - Pre-Market: 4:00ص - 9:30ص
    - Regular: 9:30ص - 4:00م
    - After-Hours: 4:00م - 8:00م
    - Closed: خارج هذي الأوقات
    """
    try:
        # yfinance يرجع index بتوقيت timezone-aware، نحوله لتوقيت نيويورك
        ny_time = timestamp.tz_convert("America/New_York")
        t = ny_time.time()

        if t < pd_time(4, 0):
            return "closed"
        elif t < pd_time(9, 30):
            return "pre-market"
        elif t < pd_time(16, 0):
            return "regular"
        elif t < pd_time(20, 0):
            return "after-hours"
        else:
            return "closed"
    except Exception:
        return "unknown"


def get_quote(symbol):
    """
    يرجع dict فيها كل البيانات المطلوبة للسهم، أو None لو فشل الجلب
    أو السهم خارج نطاق السعر المستهدف
