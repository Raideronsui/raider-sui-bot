# config.py

import os
import logging
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# === Logging Setup ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Validate & Load Required Configs ===
def get_env_var(key, default=None, required=False):
    value = os.getenv(key, default)
    if required and not value:
        logger.error(f"Missing required environment variable: {key}")
    return value

# === Primary Configs ===
SUI_PRIVATE_KEY = get_env_var("SUI_PRIVATE_KEY", required=True)
SUI_RPC_URL = get_env_var("SUI_RPC_URL", required=True)
CETUS_API = get_env_var("CETUS_API", "https://api-sui.cetus.zone")

BOT_TOKEN = get_env_var("BOT_TOKEN", required=True)
CHAT_ID = get_env_var("CHAT_ID", required=True)

# === Feature Toggles ===
ALERTS_ONLY_MODE = os.getenv("ALERTS_ONLY_MODE", "False").lower() == "true"
ENABLE_LUNAR_MODE = os.getenv("ENABLE_LUNAR_MODE", "False").lower() == "true"

# === Strategy Parameters (defaults + overrides) ===
threshold_percent = float(os.getenv("TRADE_THRESHOLD_PERCENT", 5))
take_profit_percent = float(os.getenv("TAKE_PROFIT_PERCENT", 10))
stop_loss_percent = float(os.getenv("STOP_LOSS_PERCENT", 5))

# === Dynamic setters ===
def set_threshold(value):
    global threshold_percent
    try:
        threshold_percent = float(value)
        return f"✅ Threshold set to {threshold_percent}%"
    except ValueError:
        return "❌ Invalid threshold. Please enter a number."

def get_threshold():
    return threshold_percent

# === Schedule Settings ===
SCHEDULED_INTERVAL_HOURS = int(os.getenv("SCHEDULED_INTERVAL_HOURS", 6))
SCHEDULED_TRADE_TIME_UTC = os.getenv("SCHEDULED_TRADE_TIME_UTC", "09:00")

d652510 (Fix: Add working set_threshold and config validation)
