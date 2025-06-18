import os
import logging

# === Setup logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _parse_float(env_var: str, default: float, name: str) -> float:
    try:
        return float(os.getenv(env_var, default))
    except ValueError:
        logger.warning(f"⚠️ Invalid float for {name}. Using default: {default}")
        return default

def _parse_int(env_var: str, default: int, name: str) -> int:
    try:
        return int(os.getenv(env_var, default))
    except ValueError:
        logger.warning(f"⚠️ Invalid integer for {name}. Using default: {default}")
        return default

def _parse_bool(env_var: str, default: bool, name: str) -> bool:
    value = os.getenv(env_var, str(default))
    if value.lower() in ["true", "1", "yes"]:
        return True
    elif value.lower() in ["false", "0", "no"]:
        return False
    else:
        logger.warning(f"⚠️ Invalid boolean for {name}. Using default: {default}")
        return default

def get_threshold():
    return _parse_float("TRADE_THRESHOLD_PERCENT", 5.0, "TRADE_THRESHOLD_PERCENT")

def get_take_profit():
    return _parse_float("TAKE_PROFIT_PERCENT", 10.0, "TAKE_PROFIT_PERCENT")

def get_stop_loss():
    return _parse_float("STOP_LOSS_PERCENT", 5.0, "STOP_LOSS_PERCENT")

def is_alerts_only_mode():
    return _parse_bool("ALERTS_ONLY_MODE", False, "ALERTS_ONLY_MODE")

def is_lunar_mode_enabled():
    return _parse_bool("ENABLE_LUNAR_MODE", False, "ENABLE_LUNAR_MODE")

def get_interval_hours():
    return _parse_int("SCHEDULED_INTERVAL_HOURS", 6, "SCHEDULED_INTERVAL_HOURS")

def get_scheduled_trade_time_utc():
    value = os.getenv("SCHEDULED_TRADE_TIME_UTC", "09:00")
    if not isinstance(value, str) or ":" not in value:
        logger.warning("⚠️ Invalid time format for SCHEDULED_TRADE_TIME_UTC. Using default: 09:00")
        return "09:00"
    return value

def _parse_int(env_var: str, default: int, name: str) -> int:
    try:
        return int(os.getenv(env_var, default))
    except ValueError:
        logger.warning(f"⚠️ Invalid integer for {name}. Using default: {default}")
        return default

def _parse_bool(env_var: str, default: bool, name: str) -> bool:
    value = os.getenv(env_var, str(default))
    if value.lower() in ["true", "1", "yes"]:
        return True
    elif value.lower() in ["false", "0", "no"]:
        return False
    else:
        logger.warning(f"⚠️ Invalid boolean for {name}. Using default: {default}")
        return default

def get_threshold():
    return _parse_float("TRADE_THRESHOLD_PERCENT", 5.0, "TRADE_THRESHOLD_PERCENT")

def get_take_profit():
    return _parse_float("TAKE_PROFIT_PERCENT", 10.0, "TAKE_PROFIT_PERCENT")

def get_stop_loss():
    return _parse_float("STOP_LOSS_PERCENT", 5.0, "STOP_LOSS_PERCENT")

def is_alerts_only_mode():
    return _parse_bool("ALERTS_ONLY_MODE", False, "ALERTS_ONLY_MODE")

def is_lunar_mode_enabled():
    return _parse_bool("ENABLE_LUNAR_MODE", False, "ENABLE_LUNAR_MODE")

def get_interval_hours():
    return _parse_int("SCHEDULED_INTERVAL_HOURS", 6, "SCHEDULED_INTERVAL_HOURS")

def get_scheduled_trade_time_utc():
    value = os.getenv("SCHEDULED_TRADE_TIME_UTC", "09:00")
    if not isinstance(value, str) or ":" not in value:
        logger.warning("⚠️ Invalid time format for SCHEDULED_TRADE_TIME_UTC. Using default: 09:00")
        return "09:00"
    return value
