from pathlib import Path
import threading
import time

LOG_FILE = Path(__file__).resolve().parent.parent/'artifacts'/'logs'/'daemon.log'


def tail_log():
    print("[*] LILITH Watcher Feed Activated.")
    with LOG_FILE.open('r') as f:
        f.seek(0, 2) 
        while True:
            where = f.tell()
            line = f.readline()
            if not line:
                time.sleep(0.5)
                f.seek(where)
            else:
                print(f"\r[LOG] {line.strip():<80}",end='', flush=True)
                

def start_watcher():
    t = threading.Thread(target=tail_log, daemon=True)
    t.start()