import requests
from datetime import datetime
import time
import os
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

# === TELEGRAM ===
def send_telegram_alert(message):
    """Send a Telegram alert via bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"[!] Failed to send Telegram alert: {e}")

# === PRICE FETCH ===
def fetch_price():
    """Get current price estimate from Cetus."""
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
        print(f"[{datetime.now()}] Failed to fetch price: {e}")
        return None

# === LOGIC ===
def should_buy(price_history):
    return len(price_history) >= 3 and price_history[-1] < min(price_history[-3:-1]) * 0.98

def should_sell(price_history):
    return len(price_history) >= 3 and price_history[-1] > max(price_history[-3:-1]) * 1.02

# === MAIN ENTRY ===
def execute_trade_logic():
    price_history = []
    send_telegram_alert("🟢 Raider Bot started swing trading 🪙")
    
    while True:
        price = fetch_price()
        if price:
            print(f"[{datetime.now()}] Price: {price}")
            price_history.append(price)
            
            if should_buy(price_history):
                msg = f"📉 BUY signal! Price dipped to {price:.5f} SUI"
                print(msg)
                send_telegram_alert(msg)
                
            elif should_sell(price_history):
                msg = f"📈 SELL signal! Price jumped to {price:.5f} SUI"
                print(msg)
                send_telegram_alert(msg)

        time.sleep(60)
