import sys
from pathlib import Path

# Force Add /rituals/net_mapper/ to sys.path for dynamic loading
NETMAPPER_DIR = Path(__file__).resolve().parent / 'net_mapper'
if str(NETMAPPER_DIR) not in sys.path:
    sys.path.insert(0, str(NETMAPPER_DIR))

from .net_mapper.lan_mapper import arp_scan, threaded_icmp_scan, threaded_tcp_scan
from core.logger import log_event, log_history

PARAMS = ['range', 'ports']

def run(**kwargs):
    ip_range = kwargs.get('range')
    ports = kwargs.get('ports')
    if not ip_range:
        print("[-] IP Range is required.")
        log_event("NetMap Ritual Failed - No IP range provided.")
        log_history("netmap_ritual", "Failed - No IP range provided.")
        return

    if not ports:
        ports = [80, 443, 22, 21, 23]
    else:
        ports = [int(p.strip()) for p in ports.split(',')]

    print(f"[NetMap Ritual] Starting LAN Mapping on {ip_range} with ports {ports}")
    log_event(f"NetMap Ritual initiated on {ip_range}")
    log_history("netmap_ritual", f"Initiated on {ip_range} with ports {ports}")

    live_hosts = arp_scan(ip_range)
    threaded_icmp_scan(live_hosts)
    threaded_tcp_scan(live_hosts, ports)

    print("[NetMap Ritual] Scan Complete.")
    log_event("NetMap Ritual Completed.")
    log_history("netmap_ritual", "Scan Completed.")
