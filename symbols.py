"""
يجلب قائمة رموز NASDAQ كاملة من ملف NASDAQ الرسمي المتاح للعامة،
ثم يرجع القائمة الخام (بدون فلترة سعر هنا - الفلترة تصير في market.py
بعد جلب آخر سعر، لأن القائمة الرسمية لا تحتوي على السعر الحالي).
"""

import requests

NASDAQ_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"

# قائمة احتياطية (Fallback) تستخدم في حال فشل الاتصال بمصدر NASDAQ
FALLBACK_SYMBOLS = [
    "SNDL", "NAKD", "GNUS", "ZOM", "CTRM", "TOPS", "SHIP", "NIO",
    "PLUG", "FCEL", "RIOT", "MARA", "SOS", "TRCH", "CIDM", "INPX",
]


def get_nasdaq_symbols():
    """
    يرجع قائمة رموز NASDAQ (بدون فلترة سعر).
    يستخدم ملف NASDAQ الرسمي pipe-delimited.
    """
    try:
        response = requests.get(NASDAQ_LISTED_URL, timeout=15)
        response.raise_for_status()
        lines = response.text.strip().split("\n")

        symbols = []
        for line in lines[1:-1]:  # تجاهل سطر العنوان وسطر آخر السجل (File Creation Time)
            parts = line.split("|")
            if len(parts) < 2:
                continue
            symbol = parts[0].strip()
            etf_flag = parts[5].strip() if len(parts) > 5 else "N"
            test_issue = parts[3].strip() if len(parts) > 3 else "N"

            # استبعاد ETFs والرموز التجريبية والرموز الغريبة (تحتوي على رموز خاصة)
            if etf_flag == "Y" or test_issue == "Y":
                continue
            if not symbol.isalpha():
                continue
            if len(symbol) > 5:
                continue

            symbols.append(symbol)

        if symbols:
            print(f"✅ تم جلب {len(symbols)} رمز من NASDAQ")
            return symbols

    except Exception as e:
        print(f"⚠️ فشل جلب قائمة NASDAQ: {e}")

    print(f"↩️ استخدام القائمة الاحتياطية ({len(FALLBACK_SYMBOLS)} رمز)")
    return FALLBACK_SYMBOLS


# القائمة يتم تحميلها مرة عند بدء التشغيل، وتُحدّث دورياً داخل scanner.py
SYMBOLS = get_nasdaq_symbols()
