import os
import threading
import time
import traceback

from flask import Flask

from scanner import scan_market
from telegram_bot import send_message, format_alert
from config import SCAN_INTERVAL_SECONDS

# -----------------------------
# Flask (مطلوب لـ Render Web Service)
# -----------------------------
app = Flask(__name__)

# آخر حالة فحص — تُعرض على الصفحة الرئيسية للتأكد إن البوت شغال
last_scan_status = {"time": None, "qualified_count": 0, "new_alerts_count": 0}


@app.route("/")
def home():
    return (
        "NASDAQ Momentum Scanner Running ✅<br>"
        f"آخر فحص: {last_scan_status['time']}<br>"
        f"أسهم مؤهلة حالياً: {last_scan_status['qualified_count']}<br>"
        f"تنبيهات جديدة آخر فحص: {last_scan_status['new_alerts_count']}"
    )


# -----------------------------
# حلقة الفحص الدورية
# -----------------------------
def run_scanner_loop():
    print("🚀 NASDAQ Momentum Scanner Started")
    send_message("✅ بدأ تشغيل سكانر الزخم — فحص كل "
                 f"{SCAN_INTERVAL_SECONDS // 60} دقيقة")

    while True:
        try:
            qualified, new_alerts = scan_market()

            last_scan_status["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            last_scan_status["qualified_count"] = len(qualified)
            last_scan_status["new_alerts_count"] = len(new_alerts)

            print(
                f"🔍 فحص مكتمل: {len(qualified)} سهم مؤهل، "
                f"{len(new_alerts)} تنبيه جديد"
            )

            if new_alerts:
                for stock in new_alerts:
                    send_message(format_alert(stock))

        except Exception as e:
            print("Scanner Error:", e)
            traceback.print_exc()

        time.sleep(SCAN_INTERVAL_SECONDS)


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    # تشغيل حلقة الفحص في الخلفية (thread منفصل) عشان ما توقف Flask
    threading.Thread(target=run_scanner_loop, daemon=True).start()

    # تشغيل Flask (مهم لـ Render Web Service عشان ما يطفّي الخدمة)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
