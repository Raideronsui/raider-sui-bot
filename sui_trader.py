import os
import requests
from datetime import datetime
from config import (
    TRADE_THRESHOLD_PERCENT,
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT,
    ALERTS_ONLY_MODE,
    ENABLE_LUNAR_MODE,
)

def get_price_from_cetus():
    response = requests.get(f"{os.getenv('CETUS_API')}/v2/swap/quote?inputCoinType=0x2::sui::SUI&outputCoinType=0x2::usdt::USDT&amount=100000000")
    data = response.json()
    return float(data.get('estimatedAmountOut', 0)) / 1e6  # assuming USDT 6 decimals

def moon_phase_today():
    # Placeholder lunar logic
    phases = ["🌑 New Moon", "🌓 First Quarter", "🌕 Full Moon", "🌗 Last Quarter"]
    return phases[datetime.utcnow().day % 4]

def should_trade(price_now, reference_price):
    change_percent = ((price_now - reference_price) / reference_price) * 100
    return abs(change_percent) >= TRADE_THRESHOLD_PERCENT, change_percent

def simulate_trade(price_now, change_percent):
    decision = "BUY" if change_percent < 0 else "SELL"
    target = price_now * (1 + TAKE_PROFIT_PERCENT / 100)
    stop = price_now * (1 - STOP_LOSS_PERCENT / 100)
    return {
        "action": decision,
        "price": price_now,
        "change": change_percent,
        "take_profit": round(target, 4),
        "stop_loss": round(stop, 4)
    }

def execute_trade_logic():
    try:
        price = get_price_from_cetus()
        reference_price = price * (1 - (TRADE_THRESHOLD_PERCENT / 100 + 0.01))  # simulated ref
        do_trade, change = should_trade(price, reference_price)

        if ENABLE_LUNAR_MODE:
            phase = moon_phase_today()
        else:
            phase = None

        if do_trade:
            result = simulate_trade(price, change)
            if ALERTS_ONLY_MODE:
                return f"🔔 ALERT ONLY\nPrice: ${price:.4f} | Δ {change:.2f}%\nAction: {result['action']}\nTP: {result['take_profit']} | SL: {result['stop_loss']}"
            else:
                return f"✅ TRADE EXECUTED\nPrice: ${price:.4f} | Δ {change:.2f}%\nAction: {result['action']}\nTP: {result['take_profit']} | SL: {result['stop_loss']}"
        else:
            return f⚠️ No trade signal. Price: ${price:.4f} | Δ {change:.2f}%"

    except Exception as e:
        return f"❌ Trade error: {e}"

