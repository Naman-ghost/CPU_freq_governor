# auto_cpufreq/profiles.py

import psutil
import logging

# Example profile definitions (can be extended via config)
PROFILES = {
	# done
    "default": {
        "governor": "schedutil",
        "turbo": False,
        "gpu_boost": False
    },
    # done
    "gaming": {
        "governor": "performance",
        "turbo": True,
        "gpu_boost": True
    },
    "work": {
        "governor": "ondemand",
        "turbo": True,
        "gpu_boost": False
    },
    "video_editing": {
        "governor": "performance",
        "turbo": True,
        "gpu_boost": True
    },
    # done 
    "battery_saver": {
        "governor": "powersave",
        "turbo": False,
        "gpu_boost": False
    }
}

active_profile = "default"


def detect_profile() -> str:
    """
    Auto-detects profile based on running processes.
    """
    global active_profile
    processes = [p.name().lower() for p in psutil.process_iter(attrs=['name'])]

    if any("steam" in p or "game" in p for p in processes):
        active_profile = "gaming"
    elif any("blender" in p or "davinci" in p for p in processes):
        active_profile = "video_editing"
    elif any("code" in p or "pycharm" in p for p in processes):
        active_profile = "work"
    elif "chrome" in processes and "battery" in processes:
        active_profile = "battery_saver"
    else:
        active_profile = "default"

    logging.info(f"Auto-selected profile: {active_profile}")
    return active_profile


def get_profile_settings(profile: str = None) -> dict:
    """
    Returns profile settings (governor, turbo, gpu_boost).
    """
    if profile is None:
        profile = active_profile
    return PROFILES.get(profile, PROFILES["default"])
