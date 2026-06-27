import requests
import time
import os
from telegram import Bot

# --- الإعدادات ---
# يتم جلب التوكن والآيدي من إعدادات البيئة (Environment Variables) في Render
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# إنشاء كائن البوت فقط إذا كانت المتغيرات موجودة
if TELEGRAM_TOKEN and CHAT_ID:
    bot = Bot(token=TELEGRAM_TOKEN)
else:
    print("خطأ: يرجى التأكد من إضافة TELEGRAM_TOKEN و CHAT_ID في إعدادات Render.")

def send_alert(message):
    try:
        if TELEGRAM_TOKEN and CHAT_ID:
            bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"خطأ في إرسال التليجرام: {e}")

def check_market():
    url = "https://gamma-api.polymarket.com/markets?active=true"
    try:
        response = requests.get(url)
        markets = response.json()
        
        matches = []
        
        for market in markets:
            # استخراج السعر
            price = float(market.get('lastTradePrice', 0))
            
            # الفلترة: نطاق السعر (0.20$ - 10$)
            if 0.20 <= price <= 10.0:
                question = market.get('question')
                matches.append(f"• {question} | السعر: {price:.2f}$")
        
        # إرسال تقرير مجمع إذا وُجدت نتائج
        if matches:
            final_message = "🚨 **فرص تداول جديدة (فحص كل 10 دقائق):**\n\n" + "\n".join(matches)
            send_alert(final_message)
            print(f"تم إرسال {len(matches)} فرصة جديدة.")
        else:
            print("لا توجد فرص مطابقة في هذه الدورة.")
                
    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال: {e}")

if __name__ == "__main__":
    print("الروبوت يعمل الآن ويراقب الأسواق كل 10 دقائق...")
    while True:
        check_market()
        # النوم لمدة 600 ثانية (أي 10 دقائق)
        time.sleep(600)
        
