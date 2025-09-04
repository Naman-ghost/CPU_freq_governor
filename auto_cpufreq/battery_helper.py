# auto_cpufreq/battery_helper.py

import os
import logging

BATTERY_PATH = "/sys/class/power_supply/BAT0/"

def set_charge_threshold(threshold: int) -> bool:
    """
    Set battery charge threshold (e.g., 80 means stop charging at 80%).
    Returns True if successful, False otherwise.
    """
    try:
        threshold_file = os.path.join(BATTERY_PATH, "charge_control_end_threshold")
        if os.path.exists(threshold_file):
            with open(threshold_file, "w") as f:
                f.write(str(threshold))
            logging.info(f"Battery charge threshold set to {threshold}%")
            return True
        else:
            logging.warning("Charge threshold control not supported on this device.")
            return False
    except PermissionError:
        logging.error("Permission denied. Run as root to set battery thresholds.")
        return False
    except Exception as e:
        logging.error(f"Error setting battery threshold: {e}")
        return False


def get_battery_health() -> dict:
    """
    Returns battery health details: percentage, status, wear_level (if available).
    """
    info = {"percentage": None, "status": None, "wear_level": None}

    try:
        with open(os.path.join(BATTERY_PATH, "capacity")) as f:
            info["percentage"] = int(f.read().strip())
    except FileNotFoundError:
        pass

    try:
        with open(os.path.join(BATTERY_PATH, "status")) as f:
            info["status"] = f.read().strip()
    except FileNotFoundError:
        pass

    # Battery wear estimation (only on some laptops)
    full_design = os.path.join(BATTERY_PATH, "charge_full_design")
    full_now = os.path.join(BATTERY_PATH, "charge_full")
    if os.path.exists(full_design) and os.path.exists(full_now):
        try:
            with open(full_design) as f:
                design = int(f.read().strip())
            with open(full_now) as f:
                full = int(f.read().strip())
            info["wear_level"] = round(100 - (full / design) * 100, 2)
        except Exception:
            pass

    return info
