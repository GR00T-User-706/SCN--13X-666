"""
OS-specific compatibility utilities.
"""

import platform
import sys
from pathlib import Path

def get_os():
    return platform.system()

def get_data_dir(app_name):
    """Get OS-specific data directory"""
    system = platform.system()
    
    if system == "Windows":
        return Path.home() / "AppData" / "Local" / app_name
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / app_name
    else:  # Linux/BSD
        return Path.home() / f".{app_name.lower()}"