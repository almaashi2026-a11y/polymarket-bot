import requests
import time
import os
import threading
from flask import Flask
from telegram import Bot

# --- إعداد Flask لإرضاء Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- إعدادات البوت ---
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

if TELEGRAM_TOKEN and CHAT_ID:
    bot = Bot(token=TELEGRAM_TOKEN)
else:
    print("خطأ: يرجى التأكد من إضافة TELEGRAM_TOKEN و CHAT_ID في إعدادات Render.")

def send_alert(message):
    try:
        if TELEGRAM_TOKEN and CHAT_ID:
            # استخدام async هنا سيتطلب تعديلات أكبر، لذا نستخدم الطلبات المباشرة
            requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                          data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"خطأ في إرسال التليجرام: {e}")

def check_market():
    url = "https://gamma-api.polymarket.com/markets?active=true"
    try:
        response = requests.get(url)
        markets = response.json()
        
        matches = []
        for market in markets:
            price = float(market.get('lastTradePrice', 0))
            if 0.20 <= price <= 10.0:
                question = market.get('question')
                matches.append(f"• {question} | السعر: {price:.2f}$")
        
        if matches:
            final_message = "🚨 **فرص تداول جديدة:**\n\n" + "\n".join(matches[:10]) # تقليل العدد لتجنب مشاكل الطول
            send_alert(final_message)
            print(f"تم إرسال {len(matches)} فرصة.")
    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال: {e}")

def run_bot():
    print("الروبوت يعمل الآن...")
    while True:
        check_market()
        time.sleep(600)

def run_bot():
    print("الروبوت يعمل الآن...")
    send_alert("✅ تم تشغيل البوت بنجاح على Render")
    while True:
        time.sleep(600)
