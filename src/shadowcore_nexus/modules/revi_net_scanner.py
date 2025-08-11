import sys
import os
from datetime import datetime
import traceback

try:
    from scapy.all import srp, Ether, ARP, conf
except ImportError:
    print("Scapy import error:\n")
    traceback.print_exc()
    sys.exit(1)

try:
    import netifaces
except ImportError:
    print("netifaces import error:\n")
    traceback.print_exc()
    sys.exit(1)

from core import colors
from core.messages import *

def scan():
    try:
        # Root Permission Check
        if os.geteuid() != 0:
            print_error("Root permissions required. Exiting.")
            sys.exit(1)

        # Valid Interfaces Check (Only with IPv4)
        valid_interfaces = []
        for iface in netifaces.interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(iface):
                valid_interfaces.append(iface)

        if not valid_interfaces:
            print_error("No valid interfaces with IPv4 found.")
            return

        # Display Interfaces
        print(colors.blue + "interfaces:" + colors.end)
        for iface in valid_interfaces:
            print(colors.yellow + iface + colors.end)
        print("")

        # Interface Input
        interface = input(colors.purple + "interface: " + colors.end)
        if interface not in valid_interfaces:
            print_error("Invalid interface selected.")
            return

        # Safe IP Fetch from Interface
        try:
            ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        except (ValueError, KeyError, IndexError, TypeError):
            print_error("Invalid interface or no IPv4 assigned.")
            return

        ips = ip + "/24"  # Static /24 — Future: make dynamic CIDR input
        print_info("scanning please wait...\n", start="\n")
        print(colors.blue + "MAC - IP" + colors.end)

        start_time = datetime.now()

        conf.verb = 0  # Disable Scapy verbosity
        try:
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ips),
                             timeout=2, iface=interface, inter=0.1)
        except PermissionError:
            print_error('Root permissions required')
            return

        for snd, rcv in ans:
            print(rcv.sprintf(colors.yellow + "r%Ether.src% - %ARP.psrc%" + colors.end))

        stop_time = datetime.now()
        total_time = stop_time - start_time
        print_success("scan completed", start="\n")
        print_success("scan duration: " + str(total_time))

    except KeyboardInterrupt:
        print_info("network scanner terminated", start="\n")