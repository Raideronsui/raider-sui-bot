import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables with fallback defaults
SUI_PRIVATE_KEY = os.getenv("SUI_PRIVATE_KEY")
SUI_RPC_URL = os.getenv("SUI_RPC_URL", "https://fullnode.mainnet.sui.io")
CETUS_API = os.getenv("CETUS_API", "https://api-sui.cetus.zone")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME", "")

# Strategy parameters (with dynamic update support)
threshold_percent = float(os.getenv("TRADE_THRESHOLD_PERCENT", 5))
take_profit_percent = float(os.getenv("TAKE_PROFIT_PERCENT", 10))
stop_loss_percent = float(os.getenv("STOP_LOSS_PERCENT", 5))

alerts_only_mode = os.getenv("ALERTS_ONLY_MODE", "False").lower() == "true"
enable_lunar_mode = os.getenv("ENABLE_LUNAR_MODE", "False").lower() == "true"

scheduled_interval_hours = int(os.getenv("SCHEDULED_INTERVAL_HOURS", 6))
scheduled_trade_time_utc = os.getenv("SCHEDULED_TRADE_TIME_UTC", "09:00")

# === Config updater for Telegram command support ===
def set_threshold(value):
    global threshold_percent
    try:
        threshold_percent = float(value)
        return f"✅ Threshold set to {threshold_percent}%"
    except ValueError:
        return "❌ Invalid threshold. Please enter a numeric value."

def get_threshold():
    return threshold_percent

