import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from config import from config import (
    get_threshold,
    get_take_profit,
    get_stop_loss,
    is_alerts_only_mode,
    is_lunar_mode_enabled,
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
        response.raise_for_status()
        data = response.json()
        return float(data.get('estimatedAmountOut', 0)) / 1e6  # assuming USDT has 6 decimals
    except Exception as e:
        raise RuntimeError(f"Price fetch failed: {e}")

# === LUNAR PHASES ===
def moon_phase_today():
    phases = ["🌑 New Moon", "🌓 First Quarter", "🌕 Full Moon", "🌗 Last Quarter"]
    return phases[datetime.utcnow().day % 4]

# === TRADE DECISION ===
def should_trade(price_now, reference_price):
    change_percent = ((price_now - reference_price) / reference_price) * 100
    return abs(change_percent) >= TRADE_THRESHOLD_PERCENT, change_percent

def simulate_trade(price_now, change_percent):
    decision = "BUY" if change_percent < 0 else "SELL"
    take_profit = price_now * (1 + TAKE_PROFIT_PERCENT / 100)
    stop_loss = price_now * (1 - STOP_LOSS_PERCENT / 100)
    return {
        "action": decision,
        "price": round(price_now, 4),
        "change": round(change_percent, 2),
        "take_profit": round(take_profit, 4),
        "stop_loss": round(stop_loss, 4)
    }

# === MAIN LOGIC ===
def execute_trade_logic():
    try:
        price_now = get_price_from_cetus()
        reference_price = price_now * (1 - ((TRADE_THRESHOLD_PERCENT + 1) / 100))  # simulate previous dip or pump
        do_trade, change = should_trade(price_now, reference_price)

        moon = moon_phase_today() if ENABLE_LUNAR_MODE else None

        if do_trade:
            result = simulate_trade(price_now, change)
            base_message = (
                f"{'🔔 ALERT ONLY' if ALERTS_ONLY_MODE else '✅ TRADE EXECUTED'}\n"
                f"Price: ${result['price']} | Δ {result['change']}%\n"
                f"Action: {result['action']}\n"
                f"TP: {result['take_profit']} | SL: {result['stop_loss']}"
            )
            if moon:
                base_message += f"\n🌕 Lunar Phase: {moon}"
            return base_message
        else:
            response = f"⚠️ No trade signal. Price: ${price_now:.4f} | Δ {change:.2f}%"
            if moon:
                response += f"\n🌕 Lunar Phase: {moon}"
            return response

    except Exception as e:
        return f"❌ Trade error: {e}"

