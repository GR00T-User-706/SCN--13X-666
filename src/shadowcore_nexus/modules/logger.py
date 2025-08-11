import logging
import json
from datetime import datetime

class Logger:
    def __init__(self, log_file='netmap.log', json_mode=False):
        self.json_mode = json_mode
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')
        self.log_file = log_file

    def log(self, data: dict):
        timestamp = datetime.now().isoformat()
        data['timestamp'] = timestamp

        if self.json_mode:
            log_entry = json.dumps(data)
        else:
            log_entry = f"[{timestamp}] " + ' | '.join(f"{k}: {v}" for k, v in data.items() if k != 'timestamp')

        logging.info(log_entry)
        print(log_entry)  # Console output
