import subprocess

PARAMS = ['target']

def run(**kwargs):
    target = kwargs.get('target')
    from core.logger import log_event, log_history
    
    if not target:
        print("[-] No target specified.")
        log_event("Scanner Ritual Failed - No target specified.")
        log_history("scanner", "Failed - No target specified.")
        return
        
    print(f"[Scanner Ritual] Scanning target: {target}")
    log_event(f"Scanner Ritual initiated scan on {target}")
    log_history("scanner", f"Initiated scan on {target}")

    try:
        result = subprocess.check_output(['arp', '-a'], universal_newlines=True)
        print("[Scanner Payload] ARP Scan Results:")
        print(result)
        log_event(f"ARP Scan Results:\n{result}")
        log_history("scanner", f"ARP Scan Results:\n{result}")
    except Exception as e:
        print(f"[-] Scanner Payload Error: {e}")
        log_event(f"Scanner Payload Error: {e}")
        log_history("scanner", f"Payload Error: {e}")

print("[+] Scanner Ritual Executed Successfully.")

