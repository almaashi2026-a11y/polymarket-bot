import os
import threading
from flask import Flask

from scanner import scan_market
from telegram_bot import send_message

# -----------------------------
# Flask
# -----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "NASDAQ Scanner Running ✅"

# -----------------------------
# تشغيل السكنر
# -----------------------------
def run_bot():

    print("🚀 NASDAQ Scanner Started")

    send_message("✅ بدأ فحص سوق NASDAQ")

    try:
        results = scan_market()

        if not results:
            send_message("❌ لم يتم العثور على بيانات.")
            return

        message = "📊 أفضل 5 أسهم حالياً\n\n"

        for stock in results[:5]:

            message += (
                f"📈 {stock['symbol']}\n"
                f"⭐ Score: {stock['score']}/100\n"
                f"💲 السعر: ${stock['price']}\n"
                f"📊 التغير: {stock['change_percent']:.2f}%\n\n"
            )

        send_message(message)

    except Exception as e:
        print("Scanner Error:", e)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    # تشغيل السكنر في الخلفية
    threading.Thread(
        target=run_bot,
        daemon=True
    ).start()

    # تشغيل Flask (مهم لـ Render)
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
