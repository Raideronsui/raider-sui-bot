import os
from dotenv import load_dotenv

load_dotenv()

# === Fallback defaults ===
DEFAULT_THRESHOLD = 5.0
DEFAULT_TAKE_PROFIT = 10.0
DEFAULT_STOP_LOSS = 5.0

# === Configurable Trading Parameters ===
threshold_percent = float(os.getenv("TRADE_THRESHOLD_PERCENT", DEFAULT_THRESHOLD))
take_profit_percent = float(os.getenv("TAKE_PROFIT_PERCENT", DEFAULT_TAKE_PROFIT))
stop_loss_percent = float(os.getenv("STOP_LOSS_PERCENT", DEFAULT_STOP_LOSS))

def set_threshold(value):
    global threshold_percent
    try:
        threshold_percent = float(value)
        return f"✅ Threshold set to {threshold_percent}%"
    except ValueError:
        return "❌ Invalid threshold. Please enter a number."

def get_threshold():
    return threshold_percent

def get_take_profit():
    return take_profit_percent

def get_stop_loss():
    return stop_loss_percent

# === Optional Modes ===
def get_alerts_only():
    return os.getenv("ALERTS_ONLY_MODE", "False").lower() == "true"

def get_lunar_mode():
    return os.getenv("ENABLE_LUNAR_MODE", "False").lower() == "true"
