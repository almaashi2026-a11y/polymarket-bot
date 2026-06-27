from scanner import get_stock_price
from telegram_bot import send_message

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

else:
    print("فشل الاتصال بـ Finnhub")
