"""
OS-specific compatibility utilities.
"""

import platform

def get_os():
    return platform.system()