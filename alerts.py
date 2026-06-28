"""
يدير سجل التنبيهات (JSON) لتطبيق cooldown — نفس فكرة المشروع الأساسي.
السهم اللي تم التنبيه عليه لا يُعاد التنبيه عليه إلا بعد انقضاء
ALERT_COOLDOWN_MINUTES من آخر تنبيه.
"""

import json
import os
from datetime import datetime, timedelta

from config import ALERTS_LOG_FILE, ALERT_COOLDOWN_MINUTES


def _load_log():
    if not os.path.exists(ALERTS_LOG_FILE):
        return {}
    try:
        with open(ALERTS_LOG_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ فشل قراءة سجل التنبيهات: {e}")
        return {}


def _save_log(log):
    try:
        with open(ALERTS_LOG_FILE, "w") as f:
            json.dump(log, f)
    except Exception as e:
        print(f"⚠️ فشل حفظ سجل التنبيهات: {e}")


def filter_new_alerts(stocks):
    """
    يستقبل قائمة أسهم نجحت بالفلتر، ويرجع فقط الأسهم اللي يجوز
    التنبيه عليها الآن (لم يتم التنبيه عليها سابقاً ضمن فترة الـ cooldown).
    يحدّث السجل لكل سهم يمر من الفلتر.
    """
    log = _load_log()
    now = datetime.utcnow()
    cooldown = timedelta(minutes=ALERT_COOLDOWN_MINUTES)

    new_alerts = []

    for stock in stocks:
        symbol = stock["symbol"]
        last_alert_str = log.get(symbol)

        should_alert = True
        if last_alert_str:
            try:
                last_alert_time = datetime.fromisoformat(last_alert_str)
                if now - last_alert_time < cooldown:
                    should_alert = False
            except Exception:
                pass

        if should_alert:
            new_alerts.append(stock)
            log[symbol] = now.isoformat()

    _save_log(log)
    return new_alerts
