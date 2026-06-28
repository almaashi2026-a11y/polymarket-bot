import requests

from config import TELEGRAM_TOKEN, CHAT_ID


def send_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("⚠️ TELEGRAM_TOKEN أو CHAT_ID غير مضبوطين في environment variables")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
            },
            timeout=10,
        )
    except Exception as e:
        print(f"Telegram Error: {e}")


def format_alert(stock):
    """يبني رسالة تنبيه مفصلة لسهم واحد دخل بمنطق Momentum."""
    session_labels = {
        "pre-market": "🌅 بري ماركت",
        "regular": "🔔 السوق الرسمي",
        "after-hours": "🌙 أفتر ماركت",
        "closed": "💤 السوق مغلق",
        "unknown": "السوق",
    }
    session_label = session_labels.get(stock.get("session", "unknown"), "السوق")

    dollar_vol = stock.get("dollar_volume", 0)
    if dollar_vol >= 1_000_000:
        liquidity_str = f"${dollar_vol / 1_000_000:.2f}M"
    else:
        liquidity_str = f"${dollar_vol / 1_000:.0f}K"

    return (
        f"🚀 <b>{stock['symbol']}</b> — Momentum Entry\n"
        f"⭐ Score: {stock['score']}/100\n"
        f"{session_label}\n"
        f"💲 السعر: ${stock['price']}\n"
        f"📊 تغير اليوم: {stock['change_percent']:.2f}%\n"
        f"⚡ تغير آخر 15د: +{stock['change_15m_pct']:.2f}%\n"
        f"📈 RVOL: {stock['rvol']:.2f}x\n"
        f"💧 السيولة: {liquidity_str}\n"
        f"📉 EMA9: {stock['ema9']} | VWAP: {stock['vwap']}\n"
        f"{'✅ تقاطع حديث فوق VWAP' if stock.get('ema9_crossed_above') else '✅ EMA9 فوق VWAP'}\n"
    )
