import os
from dotenv import load_dotenv

load_dotenv()

# === Config from .env with fallbacks ===
TRADE_THRESHOLD_PERCENT = float(os.getenv("TRADE_THRESHOLD_PERCENT", 5))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", 10))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", 5))
ALERTS_ONLY_MODE = os.getenv("ALERTS_ONLY_MODE", "False") == "True"
ENABLE_LUNAR_MODE = os.getenv("ENABLE_LUNAR_MODE", "False") == "True"
SCHEDULED_INTERVAL_HOURS = int(os.getenv("SCHEDULED_INTERVAL_HOURS", 6))
SCHEDULED_TRADE_TIME_UTC = os.getenv("SCHEDULED_TRADE_TIME_UTC", "09:00")

# === Dynamic setter for threshold ===
def set_threshold(new_threshold: float):
    global TRADE_THRESHOLD_PERCENT
    TRADE_THRESHOLD_PERCENT = new_threshold
