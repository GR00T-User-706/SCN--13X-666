import random
import time
from core.logger import log_event, log_history

PARAMS = ['target_range']

def run(**kwargs):
    target_range = kwargs.get('target_range')
    if not target_range:
        print("[-] No Target Range provided.")
        log_event("Simulated Mapper Failed — No target range.")
        log_history("simulated_mapper", "Failed — No target range.")
        return

    print(f"[Simulated Mapper] Scanning Range: {target_range}")
    log_event(f"Simulated Mapper started on {target_range}")
    log_history("simulated_mapper", f"Initiated on {target_range}")

    # Simulate Found Hosts
    dummy_hosts = [f"192.168.1.{i}" for i in random.sample(range(2, 254), 5)]
    for ip in dummy_hosts:
        print(f"[*] Host Found: {ip}")
        log_event(f"Host Found: {ip}")
        log_history("simulated_mapper", f"Host Found: {ip}")
        time.sleep(0.5)

    # Simulate Open Ports
    for ip in dummy_hosts:
        open_ports = random.sample([22, 80, 443, 8080, 3306], 2)
        for port in open_ports:
            print(f"[+] Open Port Found on {ip}: {port}")
            log_event(f"Open Port on {ip}: {port}")
            log_history("simulated_mapper", f"Open Port on {ip}: {port}")
            time.sleep(0.3)

    print("[Simulated Mapper] Scan Complete.")
    log_event("Simulated Mapper completed scan.")
    log_history("simulated_mapper", "Scan Completed.")
