import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# === ENV-DRIVEN CONFIG DEFAULTS ===
def parse_bool(value):
    return str(value).lower() in ["true", "1", "yes"]

# === Globals for Dynamic Config ===
threshold_percent = float(os.getenv("TRADE_THRESHOLD_PERCENT", 5))
take_profit_percent = float(os.getenv("TAKE_PROFIT_PERCENT", 10))
stop_loss_percent = float(os.getenv("STOP_LOSS_PERCENT", 5))
alert_mode = parse_bool(os.getenv("ALERTS_ONLY_MODE", "False"))
lunar_mode = parse_bool(os.getenv("ENABLE_LUNAR_MODE", "False"))

# === Accessors ===
def get_threshold_percent():
    return float(os.getenv("THRESHOLD_PERCENT", 2.0))

def get_take_profit():
    return take_profit_percent

def get_stop_loss():
    return stop_loss_percent

def is_alerts_only_mode():
    return alert_mode

def get_moon_mode():
    return os.getenv("MOON_MODE", "false").lower() == "true"

# === Dynamic Setters ===
def set_threshold(value):
    global threshold_percent
    try:
        threshold_percent = float(value)
        return f"✅ Threshold set to {threshold_percent}%"
    except ValueError:
        return "❌ Invalid threshold. Please enter a number."

def set_alert_mode(value: str):
    global alert_mode
    if value.lower() in ["true", "false"]:
        alert_mode = value.lower() == "true"
        return f"✅ Alerts-only mode set to {alert_mode}"
    return "❌ Invalid value. Use true or false."

def set_take_profit(value):
    global take_profit_percent
    try:
        take_profit_percent = float(value)
        return f"✅ Take-profit set to {take_profit_percent}%"
    except ValueError:
        return "❌ Invalid value. Please enter a number."

def set_stop_loss(value):
    global stop_loss_percent
    try:
        stop_loss_percent = float(value)
        return f"✅ Stop-loss set to {stop_loss_percent}%"
    except ValueError:
        return "❌ Invalid value. Please enter a number."

def set_lunar_mode(value: str):
    global lunar_mode
    if value.lower() in ["true", "false"]:
        lunar_mode = value.lower() == "true"
        return f"🌕 Lunar mode set to {lunar_mode}"
    return "❌ Invalid value. Use true or false."

# === Validation Logging (optional) ===
def validate_env():
    keys = [
        "SUI_PRIVATE_KEY", "SUI_RPC_URL", "CETUS_API", "BOT_TOKEN", "CHAT_ID"
    ]
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        print(f"⚠️ Missing required environment variables: {', '.join(missing)}")

validate_env()

def get_alerts_only():
    return os.getenv("ALERTS_ONLY_MODE", "False").lower() == "true"

def is_alerts_only():
    return get_alerts_only()
moon_mode = os.getenv("MOON_MODE", "false").lower() == "true"

def set_moon_mode(value):
    global moon_mode
    moon_mode = str(value).lower() == "true"
    return f"🌕 Moon Mode set to {'ON' if moon_mode else 'OFF'}"

def is_moon_mode():
    return moon_mode
