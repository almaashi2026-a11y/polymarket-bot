import os

FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# -----------------------------
# إعدادات السكانر
# -----------------------------

# نطاق سعر الأسهم المستهدفة (Penny Stocks)
MIN_PRICE = 0.20
MAX_PRICE = 10.0

# شروط الدخول (Momentum Entry)
RVOL_THRESHOLD = 2.0          # حجم نسبي > 2x المعدل
PRICE_CHANGE_15M_THRESHOLD = 5.0   # تغير السعر آخر 15 دقيقة >= +5%

# مهلة التبريد بين تنبيهين لنفس السهم (بالدقائق)
ALERT_COOLDOWN_MINUTES = 60

# عدد الشموع (1-minute candles) المطلوبة لحساب EMA9/VWAP/RVOL
LOOKBACK_MINUTES = 90

# دورية الفحص (بالثواني)
SCAN_INTERVAL_SECONDS = 120

# ملف تخزين سجل التنبيهات (لتطبيق الـ cooldown)
ALERTS_LOG_FILE = "alerts_log.json"
