import os

def get_threshold():
    return float(os.getenv("TRADE_THRESHOLD_PERCENT", 5.0))

def get_take_profit():
    return float(os.getenv("TAKE_PROFIT_PERCENT", 10.0))

def get_stop_loss():
    return float(os.getenv("STOP_LOSS_PERCENT", 5.0))

def is_alerts_only_mode():
    return os.getenv("ALERTS_ONLY_MODE", "False").lower() == "true"

def is_lunar_mode_enabled():
    return os.getenv("ENABLE_LUNAR_MODE", "False").lower() == "true"

def get_interval_hours():
    return int(os.getenv("SCHEDULED_INTERVAL_HOURS", 6))

def get_scheduled_trade_time_utc():
    return os.getenv("SCHEDULED_TRADE_TIME_UTC", "09:00")
