import threading
import os
from flask import Flask

from scanner import get_stock_price
from telegram_bot import send_message

# -----------------------------
# Flask
# -----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Scanner is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# -----------------------------
# تشغيل البوت
# -----------------------------
def run_bot():

    print("🚀 NASDAQ Scanner Started")

    stock = get_stock_price("NVDA")

    if stock:

        message = f"""
✅ Finnhub متصل

السهم: {stock['symbol']}
السعر: ${stock['price']}
أعلى سعر: ${stock['high']}
أقل سعر: ${stock['low']}
"""

        print(message)

        send_message(message)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    run_bot()
