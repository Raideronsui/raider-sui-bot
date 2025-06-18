import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_env_float(var_name: str, default: float) -> float:
    try:
        return float(os.getenv(var_name, default))
    except ValueError:
        logger.warning(f"Invalid float for {var_name}. Using default: {default}")
        return default

def _get_env_int(var_name: str, default: int) -> int:
    try:
        return int(os.getenv(var_name, default))
    except ValueError:
        logger.warning(f"Invalid int for {var_name}. Using default: {default}")
        return default

def _get_env_bool(var_name: str, default: bool = False) -> bool:
    value = os.getenv(var_name)
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes", "on")

# === BOT & API ===
def get_bot_token():
    token = os.getenv("BOT_TOKEN")
    if not token:
        logger.error("Missing BOT_TOKEN in .env!")
    return token

def get_webhook_url():
    return os.getenv("WEBHOOK_URL", "")

# === TRADING SETTINGS ===
def get_threshold_percent():
    return _get_env_float("TRADE_THRESHOLD_PERCENT", 5.0)

def get_take_profit():
    return _get_env_float("TAKE_PROFIT_PERCENT", 10.0)

def get_stop_loss():
    return _get_env_float("STOP_LOSS_PERCENT", 5.0)

def get_cooldown_seconds():
    return _get_env_int("TRADE_COOLDOWN_SECONDS", 3600)

# === SUI Wallet & RPC ===
def get_sui_private_key():
    key = os.getenv("SUI_PRIVATE_KEY")
    if not key:
        logger.error("Missing SUI_PRIVATE_KEY in .env!")
    return key

def get_sui_rpc_url():
    return os.getenv("SUI_RPC_URL", "https://rpc-mainnet.suiscan.xyz:443")

# === MODE FLAGS ===
def is_alerts_only_mode():
    return _get_env_bool("ALERTS_ONLY", False)

def get_alerts_only():
    return is_alerts_only_mode()

def get_moon_mode():
    return _get_env_bool("MOON_MODE", False)

def get_test_mode():
    return _get_env_bool("TEST_MODE", True)

# === Logging control ===
def enable_debug_logging():
    logging.getLogger().setLevel(logging.DEBUG)
    logger.debug("Debug logging enabled.")

