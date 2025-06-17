# config.py

from collections import defaultdict

# In-memory user settings (for testing — should be stored in a database in production)
user_thresholds = defaultdict(lambda: 5.0)  # Default to 5%
user_alert_mode = defaultdict(lambda: False)
user_moon_mode = defaultdict(lambda: False)

# === Threshold ===
def set_threshold(user_id: int, value: float):
    user_thresholds[user_id] = value

def get_threshold(user_id: int) -> float:
    return user_thresholds[user_id]

# === Alerts Only Mode ===
def set_alert_mode(user_id: int, enabled: bool):
    user_alert_mode[user_id] = enabled

def is_alerts_only(user_id: int) -> bool:
    return user_alert_mode[user_id]

# === Lunar Mode ===
def set_moon_mode(user_id: int, enabled: bool):
    user_moon_mode[user_id] = enabled

def is_moon_mode(user_id: int) -> bool:
    return user_moon_mode[user_id]
