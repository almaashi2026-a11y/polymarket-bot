import requests
import time
from telegram import Bot

# --- الإعدادات ---
# ملاحظة: ضع الـ Token والـ Chat ID الخاصين بك هنا
TELEGRAM_TOKEN = "AAHwM-h4Pi7taJNVQZvLbma-5Id9BaJ5X6Y"
CHAT_ID = "8524780143"
bot = Bot(token=TELEGRAM_TOKEN)

def send_alert(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"خطأ في إرسال التليجرام: {e}")

def check_market():
    url = "https://gamma-api.polymarket.com/markets?active=true"
    try:
        response = requests.get(url)
        markets = response.json()
        
        # قائمة لتجميع الأسواق المطابقة في هذه الدورة
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
            # دمج النتائج في رسالة واحدة
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
        
