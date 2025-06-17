import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from config import (
    TRADE_THRESHOLD_PERCENT,
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT,
    ALERTS_ONLY_MODE,
    ENABLE_LUNAR_MODE,
    SCHEDULED_TRADE_TIME_UTC
)

# === CETUS PRICE FETCH ===
def get_price_from_cetus():
    try:
        response = requests.get(
            f"{os.getenv('CETUS_API')}/v2/swap/quote",
            params={
                "inputCoinType": "0x2::sui::SUI",
                "outputCoinType": "0x2::usdt::USDT",
                "amount": "100000000"
            }
        )
        data = response.json()
        return float(data.get("estimatedAmountOut", 0)) / 1e6  # USDT is 6 decimals
    except Exception as e:
        raise RuntimeError(f"Price fetch failed: {e}")

# === LUNAR PHASE (fun mode) ===
def moon_phase_today():
    phases = ["🌑 New Moon", "🌓 First Quarter", "🌕 Full Moon", "🌗 Last Quarter"]
    return phases[datetime.utcnow().day % 4]

# === TRADE DECISION LOGIC ===
def should_trade(price_now, reference_price):
    change_percent = ((price_now - reference_price) / reference_price) * 100
    return abs(change_percent) >= TRADE_THRESHOLD_PERCENT, change_percent

def simulate_trade(price_now, change_percent):
    decision = "BUY" if change_percent < 0 else "SELL"
    take_profit = price_now * (1 + TAKE_PROFIT_PERCENT / 100)
    stop_loss = price_now * (1 - STOP_LOSS_PERCENT / 100)
    return {
        "action": decision,
        "price": price_now,
        "change": round(change_percent, 2),
        "take_profit": round(take_profit, 4),
        "stop_loss": round(stop_loss, 4)
    }

# === CONVERT TO SCHEDULED UTC TIME (from EST string) ===
def get_scheduled_utc():
    try:
        est_hour, est_minute = map(int, SCHEDULED_TRADE_TIME_UTC.split(":"))
        est_time = datetime.now(ZoneInfo("America/New_York")).replace(hour=est_hour, minute=est_minute, second=0, microsecond=0)
        utc_time = est_time.astimezone(ZoneInfo("UTC"))
        return utc_time.time()
    except Exception as e:
        raise ValueError(f"Invalid scheduled trade time: {e}")

# === MAIN LOGIC FOR /trade ===
def execute_trade_logic():
    try:
        price = get_price_from_cetus()
        reference_price = price * (1 - (TRADE_THRESHOLD_PERCENT / 100 + 0.01))  # simulated previous
        do_trade, change = should_trade(price, reference_price)
        lunar_note = moon_phase_today() if ENABLE_LUNAR_MODE else None

        if do_trade:
            result = simulate_trade(price, change)
            mode = "🔔 ALERT ONLY" if ALERTS_ONLY_MODE else "✅ TRADE EXECUTED"
            response = f"{mode}"
Price: ${price:.4f} | Δ {result['change']}%
Action: {result['action']}
TP: {result['take_profit']} | SL: {result['stop_loss']}"
            if lunar_note:
                response += f"
🌕 Lunar Phase: {lunar_note}"
            return response
        else:
            return f"⚠️ No trade signal.
Price: ${price:.4f} | Δ {change:.2f}%"
    except Exception as e:
        return f"❌ Trade error: {e}"
