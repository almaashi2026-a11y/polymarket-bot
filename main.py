import requests
import time
import os
import threading
from flask import Flask

# -----------------------------
# Flask (لإبقاء Render يعمل)
# -----------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# -----------------------------
# إعدادات تيليجرام
# -----------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not TELEGRAM_TOKEN:
    print("❌ TELEGRAM_TOKEN غير موجود")
if not CHAT_ID:
    print("❌ CHAT_ID غير موجود")

# -----------------------------
# إرسال رسالة تيليجرام
# -----------------------------
def send_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        response = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "Markdown"
            },
            timeout=20
        )

        print("Telegram:", response.text)

    except Exception as e:
        print("خطأ في إرسال الرسالة:", e)

# -----------------------------
# فحص الأسواق
# -----------------------------
def check_market():
    try:
        url = "https://gamma-api.polymarket.com/markets?active=true"

        response = requests.get(url, timeout=20)
        markets = response.json()

        matches = []

        for market in markets:

            try:
                price = float(market.get("lastTradePrice", 0))
            except:
                continue

            if 0.20 <= price <= 10:

                question = market.get("question", "Unknown")

                matches.append(
                    f"• {question}\nالسعر: ${price:.2f}"
                )

        if matches:

            message = "🚨 فرص جديدة:\n\n"

            message += "\n\n".join(matches[:10])

            send_alert(message)

            print("تم إرسال رسالة")

        else:
            print("لا توجد فرص")

    except Exception as e:
        print("خطأ:", e)

# -----------------------------
# تشغيل البوت
# -----------------------------
def run_bot():

    print("✅ الروبوت يعمل الآن")

    send_alert("✅ تم تشغيل البوت بنجاح على Render")

    while True:

        check_market()

        time.sleep(600)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":

    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    run_bot()
