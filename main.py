import requests
import time

def check_market_status():
    # الرابط لجلب الأسواق النشطة
    url = "https://gamma-api.polymarket.com/markets?active=true"
    
    try:
        response = requests.get(url)
        markets = response.json()
        
        print("--- بدء فحص الأسواق (النطاق: 0.20$ - 10.00$) ---")
        found_count = 0
        
        for market in markets:
            # استخراج السعر وتحويله لنوع رقمي
            price_str = market.get('lastTradePrice', '0')
            price = float(price_str)
            
            # فلترة الأسواق بناءً على طلبك
            if 0.20 <= price <= 10.0:
                print(f"سوق مناسب: {market.get('question')} | السعر: {price:.2f}")
                found_count += 1
        
        if found_count == 0:
            print("لم يتم العثور على أسواق في هذا النطاق حالياً.")
            
    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال: {e}")

if __name__ == "__main__":
    # تشغيل الفحص
    check_market_status()
    
