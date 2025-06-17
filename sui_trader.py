import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# === ENV SETUP ===
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# === CETUS CONFIG ===
BASE_TOKEN = "0x2::sui::SUI"
QUOTE_TOKEN = "0xabc...xyz"  # Replace with actual token
TRADE_PAIR = f"{BASE_TOKEN}-{QUOTE_TOKEN}"
CETUS_API_URL = "https://api-sui.cetus.zone/v2/swap/price"

# === PRICE FETCH ===
def fetch_price():
    params = {
        "inputCoin": BASE_TOKEN,
        "outputCoin": QUOTE_TOKEN,
        "amount": "100000000"
    }
    try:
        response = requests.get(CETUS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data["data"]["estimatedAmountOut"]) / 1e9
    except Exception as e:
        return None

# === SIMPLE STRATEGY ===
def analyze_trend(prices):
    if len(prices) < 3:
        return "Not enough data"
    if prices[-1] < min(prices[-3:-1]) * 0.98:
        return f"📉 BUY signal at {prices[-1]:.5f} SUI"
    elif prices[-1] > max(prices[-3:-1]) * 1.02:
        return f"📈 SELL signal at {prices[-1]:.5f} SUI"
    else:
        return f"🤖 HOLD — Latest price: {prices[-1]:.5f} SUI"

# === MAIN ENTRY FOR TELEGRAM ===
def execute_trade_logic():
    prices = []

    # Simulate recent history
    for _ in range(3):
        p = fetch_price()
        if p:
            prices.append(p)

    if not prices or len(prices) < 3:
        return "⚠️ Not enough price data to analyze."

    return analyze_trend(prices)

