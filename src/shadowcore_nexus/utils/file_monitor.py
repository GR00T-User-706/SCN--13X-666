"""
Filesystem watcher for detecting new modules in the HUB directory.
"""

import os
import time

def watch_hub_directory(callback, path, interval=2):
    seen = set(os.listdir(path))
    while True:
        time.sleep(interval)
        current = set(os.listdir(path))
        new_files = current - seen
        if new_files:
            for f in new_files:
                callback(f)
        seen = current