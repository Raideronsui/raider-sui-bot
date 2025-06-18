import os
from dotenv import load_dotenv

load_dotenv()

# === SUI / Cetus Trading Config ===
SUI_PRIVATE_KEY = os.getenv("SUI_PRIVATE_KEY")
SUI_RPC_URL = os.getenv("SUI_RPC_URL", "https://fullnode.mainnet.sui.io")
CETUS_API = os.getenv("CETUS_API", "https://api-sui.cetus.zone")

# === Trading Logic Parameters ===
TRADE_THRESHOLD_PERCENT = float(os.getenv("TRADE_THRESHOLD_PERCENT", 5))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", 10))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", 5))

ALERTS_ONLY_MODE = os.getenv("ALERTS_ONLY_MODE", "False").lower() == "true"
ENABLE_LUNAR_MODE = os.getenv("ENABLE_LUNAR_MODE", "False").lower() == "true"

# === Scheduler Defaults ===
SCHEDULED_INTERVAL_HOURS = int(os.getenv("SCHEDULED_INTERVAL_HOURS", 6))
SCHEDULED_TRADE_TIME_UTC = os.getenv("SCHEDULED_TRADE_TIME_UTC", "09:00")

# === Telegram Bot Settings ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

