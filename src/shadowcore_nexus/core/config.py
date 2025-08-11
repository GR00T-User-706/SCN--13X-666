import sys
from pathlib import Path

# === Absolute Path Override ===
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path = [str(ROOT_DIR)] + sys.path  # Force ShadowCore to be sys.path[0]

import json

import json
from core.paths import CONFIGS_DIR


# Ensure ShadowCore is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


CONFIG_FILE = CONFIGS_DIR / 'daemon_config.json'

DEFAULT_CONFIG = {
    "debug_mode": True,
    "default_output_format": "txt",
    "network_timeout": 5,
    "log_level": "INFO",
    "modules_enabled": ["encoding", "scanner", "reverse_shell"]
}

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_config(config_data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)

# Auto-load on import
config = load_config()

# Optional Debug Print
if __name__ == "__main__":
    print(f"Loaded Config: {config}")
