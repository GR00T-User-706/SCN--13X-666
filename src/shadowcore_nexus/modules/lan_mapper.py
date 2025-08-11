import scapy.all as scapy
import socket
import subprocess
import threading
from pathlib import path
from logger import Logger

logger = Logger(log_file='lan_scan.log', json_mode=False)

def arp_scan(ip_range):
    print(f"[*] Starting ARP Scan on {ip_range}")
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

    live_hosts = []
    for element in answered_list:
        ip = element[1].psrc
        mac = element[1].hwsrc
        logger.log({'IP': ip, 'MAC': mac, 'Method': 'ARP'})
        live_hosts.append(ip)
    return live_hosts

def icmp_ping(host):
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-W", "1", host], stderr=subprocess.DEVNULL)
        logger.log({'IP': host, 'Method': 'ICMP', 'Status': 'Alive'})
        return True
    except subprocess.CalledProcessError:
        return False

def tcp_syn_scan(ip, ports=[80, 443, 22, 21, 23]):
    syn_packet = scapy.IP(dst=ip)/scapy.TCP(dport=ports, flags="S")
    response = scapy.sr(syn_packet, timeout=1, verbose=False)[0]

    for sent, received in response:
        if received.haslayer(scapy.TCP) and received.getlayer(scapy.TCP).flags == 0x12:
            logger.log({'IP': ip, 'Port': sent.dport, 'Method': 'TCP SYN', 'Status': 'Open'})
            # Send RST to gracefully close
            scapy.sr(scapy.IP(dst=ip)/scapy.TCP(dport=sent.dport, flags="R"), timeout=1, verbose=False)

def threaded_icmp_scan(ip_list):
    threads = []
    for ip in ip_list:
        thread = threading.Thread(target=icmp_ping, args=(ip,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

def threaded_tcp_scan(ip_list, ports):
    threads = []
    for ip in ip_list:
        thread = threading.Thread(target=tcp_syn_scan, args=(ip, ports))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LAN Mapper - ARP, ICMP, TCP Scanner")
    parser.add_argument("--range", required=True, help="Target IP Range (e.g., 192.168.1.0/24)")
    parser.add_argument("--ports", nargs="+", type=int, default=[80, 443, 22, 21, 23], help="Ports to scan via TCP SYN")
    parser.add_argument("--log", default="lan_scan.log", help="Log file path")
    args = parser.parse_args()

    logger = Logger(log_file=args.log, json_mode=False)

    live_hosts = arp_scan(args.range)
    threaded_icmp_scan(live_hosts)
    threaded_tcp_scan(live_hosts, args.ports)

    print("[*] Scan Completed. Results logged.")
