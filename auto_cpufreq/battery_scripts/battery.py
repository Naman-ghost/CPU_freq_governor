#!/usr/bin/env python3

import os
import glob
import subprocess
import logging
import time

from auto_cpufreq.battery_scripts.ideapad_acpi import (
    ideapad_acpi_print_thresholds, ideapad_acpi_setup
)
from auto_cpufreq.battery_scripts.ideapad_laptop import (
    ideapad_laptop_print_thresholds, ideapad_laptop_setup
)
from auto_cpufreq.battery_scripts.thinkpad import (
    thinkpad_print_thresholds, thinkpad_setup
)

# -------------------------
# Setup Logging
# -------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# -------------------------
# Kernel Module Checker
# -------------------------
def is_module_loaded(module_name):
    """Check if a kernel module is currently loaded."""
    try:
        result = subprocess.run(['lsmod'], stdout=subprocess.PIPE, text=True)
        return module_name in result.stdout
    except Exception as e:
        logging.error(f"Failed to check modules: {e}")
        return False


# -------------------------
# Battery Management
# -------------------------
def get_battery_thresholds():
    """Print battery charge thresholds depending on the active kernel module."""
    logging.info("Checking battery thresholds...")
    if is_module_loaded("ideapad_acpi"):
        ideapad_acpi_print_thresholds()
    elif is_module_loaded("ideapad_laptop"):
        ideapad_laptop_print_thresholds()
    elif is_module_loaded("thinkpad_acpi"):
        thinkpad_print_thresholds()
    else:
        logging.warning("No supported battery management module found.")


def setup_battery_charging():
    """Set battery charging thresholds depending on the laptop type."""
    logging.info("Setting battery thresholds...")
    if is_module_loaded("ideapad_acpi"):
        ideapad_acpi_setup()
    elif is_module_loaded("ideapad_laptop"):
        ideapad_laptop_setup()
    elif is_module_loaded("thinkpad_acpi"):
        thinkpad_setup()
    else:
        logging.warning("No supported battery module found. Setup skipped.")


# -------------------------
# CPU Frequency Monitor
# -------------------------
def print_cpu_frequencies():
    """Print the current frequency of each CPU core."""
    cpu_paths = glob.glob("/sys/devices/system/cpu/cpu[0-9]*/cpufreq/scaling_cur_freq")

    if not cpu_paths:
        logging.warning("CPU frequency info not available. Is cpufreq enabled?")
        return

    logging.info("Current CPU Frequencies (MHz):")
    for path in sorted(cpu_paths):
        try:
            with open(path, 'r') as f:
                freq_khz = int(f.read().strip())
                cpu = os.path.basename(os.path.dirname(path))
                print(f"{cpu}: {freq_khz // 1000} MHz")
        except Exception as e:
            logging.error(f"Error reading {path}: {e}")


# -------------------------
# Optional: Live Monitor
# -------------------------
def live_cpu_monitor(interval=2):
    """Continuously display CPU frequencies every `interval` seconds."""
    logging.info("Starting live CPU frequency monitor. Press Ctrl+C to stop.")
    try:
        while True:
            os.system("clear")
            print_cpu_frequencies()
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


# -------------------------
# Main Entry Point
# -------------------------
if __name__ == "__main__":
    # Print battery thresholds
    get_battery_thresholds()

    # Set up battery thresholds
    setup_battery_charging()

    # Print current CPU frequencies
    print_cpu_frequencies()

    # Optional: Uncomment to run live CPU monitor
    # live_cpu_monitor()

