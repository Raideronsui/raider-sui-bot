import requests
import logging
from config import (
    get_threshold_percent,
    get_take_profit,
    get_stop_loss,
    get_max_trades,
    is_alerts_only_mode,
    get_alerts_only,
    get_moon_mode,
    get_rpc_url,
    get_private_key,
)

# Cetus API endpoint example
CETUS_PRICE_API = "https://api-sui.cetus.zone/v2/swap/price"

def fetch_price(pair="SUI-USDC"):
    try:
        response = requests.get(f"{CETUS_PRICE_API}?pair={pair}")
        data = response.json()
        return float(data["data"]["price"])
    except Exception as e:
        logging.error(f"Price fetch error: {e}")
        return None

def get_wallet_address_from_private_key():
    try:
        # For now, just mock. Replace with real logic using `sui` SDK.
        return "0x" + get_private_key()[-40:]
    except Exception as e:
        logging.error(f"Wallet fetch error: {e}")
        return "Unavailable"

def execute_trade_logic():
    price = fetch_price()
    if price is None:
        return "❌ Failed to fetch price data."

    message = f"📊 Current SUI Price: {price:.4f} USDC"

    if get_alerts_only():
        return f"{message}\n🔔 Alerts-only mode is enabled."

    # Simulated trading logic
    threshold = get_threshold_percent()
    take_profit = get_take_profit()
    stop_loss = get_stop_loss()
    wallet = get_wallet_address_from_private_key()

    trade_message = (
        f"{message}\n"
        f"🎯 Threshold: {threshold}%\n"
        f"💰 Take Profit: {take_profit}%\n"
        f"🛡️ Stop Loss: {stop_loss}%\n"
        f"👛 Wallet: {wallet}\n"
        f"🚀 Moon Mode: {'ON' if get_moon_mode() else 'OFF'}"
    )

    return trade_message
