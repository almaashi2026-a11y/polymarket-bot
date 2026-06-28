"""
منطق الدخول (Momentum Entry) — نفس فلسفة المشروع الأساسي:
السهم لازم يكون فيه "زخم مؤكد يحدث الآن"، مو "تجميع محتمل".

الشروط الثلاثة الأساسية (لازم تتحقق كلها معاً):
1. EMA9 يقطع فوق VWAP (أو فوقه حالياً مع تقاطع حديث)
2. RVOL > 2x (حجم تداول أعلى من المعدل بضعف على الأقل)
3. تغير السعر خلال آخر 15 دقيقة >= +5%

الأسهم اللي ما تحقق الثلاثة شروط مع بعض تُستبعد بالكامل من نتائج الفحص.
"""

from config import RVOL_THRESHOLD, PRICE_CHANGE_15M_THRESHOLD

# أوزان لعرض "قوة" الإشارة فقط (للترتيب) — ما تُستخدم للاستبعاد
# السيولة مضافة كعامل تقييم بدون استبعاد: سهم بسيولة ضعيفة يدخل القائمة
# لو حقق شروط الدخول، بس درجته تكون أقل (خطر انزلاق سعري أعلى عند الدخول/الخروج)
WEIGHTS = {
    "ema9_cross": 30,
    "rvol": 25,
    "momentum_15m": 25,
    "liquidity": 20,
}


def passes_entry_filter(stock):
    """
    يرجع True فقط لو السهم يحقق الثلاثة شروط الأساسية معاً.
    هذا هو الفلتر الصارم — أي سهم يفشل بشرط واحد يُستبعد بالكامل.
    """
    ema9_ok = stock.get("ema9_above_vwap", False)
    rvol_ok = stock.get("rvol", 0) > RVOL_THRESHOLD
    momentum_ok = stock.get("change_15m_pct", 0) >= PRICE_CHANGE_15M_THRESHOLD

    return ema9_ok and rvol_ok and momentum_ok


def calculate_score(stock):
    """
    يحسب درجة قوة الإشارة (0-100) لأغراض الترتيب فقط.
    يُستخدم بعد التأكد من أن السهم نجح في passes_entry_filter().
    """
    score = 0

    # قوة تقاطع EMA9/VWAP — تقاطع حديث يستحق وزن كامل، فوق فقط بدون تقاطع حديث وزن أقل
    if stock.get("ema9_crossed_above", False):
        score += WEIGHTS["ema9_cross"]
    elif stock.get("ema9_above_vwap", False):
        score += WEIGHTS["ema9_cross"] * 0.6

    # قوة RVOL — كل ما زاد عن العتبة، زادت النقاط (حد أعلى عند 5x)
    rvol = stock.get("rvol", 0)
    if rvol > RVOL_THRESHOLD:
        rvol_ratio = min((rvol - RVOL_THRESHOLD) / (5.0 - RVOL_THRESHOLD), 1.0)
        score += WEIGHTS["rvol"] * (0.5 + 0.5 * rvol_ratio)

    # قوة الزخم خلال 15 دقيقة — كل ما زاد التغير، زادت النقاط (حد أعلى عند +20%)
    change_15m = stock.get("change_15m_pct", 0)
    if change_15m >= PRICE_CHANGE_15M_THRESHOLD:
        momentum_ratio = min(
            (change_15m - PRICE_CHANGE_15M_THRESHOLD) / (20.0 - PRICE_CHANGE_15M_THRESHOLD),
            1.0,
        )
        score += WEIGHTS["momentum_15m"] * (0.5 + 0.5 * momentum_ratio)

    # قوة السيولة (Dollar Volume) — كل ما زادت السيولة، زادت النقاط
    # سهم بسيولة ضعيفة ما يُستبعد، بس يحصل نقاط أقل (= خطر دخول/خروج أعلى)
    # سلم لوغاريتمي مستمر: من $10K (=0 نقطة تقريباً) إلى $10M (=نقاط كاملة)
    dollar_volume = stock.get("dollar_volume", 0)
    if dollar_volume > 0:
        import math
        floor_volume = 10_000
        ceiling_volume = 10_000_000
        clamped = max(min(dollar_volume, ceiling_volum
