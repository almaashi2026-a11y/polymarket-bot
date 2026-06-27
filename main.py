# هذا هو أول كود لاختبار الاتصال بمنصة Polymarket
import requests

def test_connection():
    url = "https://gamma-api.polymarket.com/events"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("نجاح: تم الاتصال بنجاح بـ Polymarket!")
        else:
            print(f"فشل الاتصال: كود الحالة {response.status_code}")
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    test_connection()
  
