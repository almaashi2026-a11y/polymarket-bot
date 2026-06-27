import requests
import time

# هذا الرابط لجلب بيانات السوق العامة من Polymarket
API_URL = "https://gamma-api.polymarket.com/markets?active=true"

def check_market_status():
    try:
        response = requests.get(API_URL)
        markets = response.json()
        
        # هنا سنقوم لاحقاً بإضافة الحسابات الرياضية للمؤشر
        for market in markets[:3]: # فحص أول 3 أسواق كمثال
            print(f"فحص السوق: {market.get('question')}")
            # هنا ستتم إضافة منطق VWAP و EMA9
            
    except Exception as e:
        print(f"حدث خطأ: {e}")

# حلقة تكرار بسيطة تجعل البوت يعمل باستمرار
if __name__ == "__main__":
    while True:
        check_market_status()
        time.sleep(60) # الروبوت يفحص السوق كل دقيقة
