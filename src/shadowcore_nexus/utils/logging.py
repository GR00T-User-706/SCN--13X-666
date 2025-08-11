from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / 'artifacts' / 'logs' / 'daemon.log'

def log_event(message):
    with LOG_FILE.open('a') as f:
        f.write(f"{message}\n")

from datetime import datetime

HISTORY_DIR = Path(__file__).resolve().parent.parent / 'artifacts' / 'history'

def log_history(ritual_name, details):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{ritual_name}_{timestamp}.log"
    filepath = HISTORY_DIR / filename

    with filepath.open('w') as f:
        f.write(f"Ritual: {ritual_name}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Details: {details}\n")