import sys
import os
from datetime import datetime
import traceback

# Import colors and custom messages
from core import colors
from core.messages import *

# Root permission check (must be at the top)
if os.geteuid() != 0:
    print_error("Root permissions required. Exiting.")
    sys.exit(1)

# Import scapy with error handling
try:
    from scapy.all import srp, Ether, ARP, conf
except ImportError:
    print(colors.red + 'Scapy import error:\n')
    traceback.print_exc()
    print(colors.end)
    sys.exit(1)

# Import netifaces with error handling
try:
    import netifaces
except ImportError:
    print(colors.red + 'netifaces import error:\n')
    traceback.print_exc()
    print(colors.end)
    sys.exit(1)


def scan():
    try:
        # Get valid interfaces with IPv4
        valid_interfaces = []
        for iface in netifaces.interfaces():
            if netifaces.AF_INET in netifaces.ifaddresses(iface):
                valid_interfaces.append(iface)

        if not valid_interfaces:
            print_error("No valid interfaces with IPv4 found.")
            return

        # Display interfaces
        print(colors.blue + "interfaces:" + colors.end)
        for iface in valid_interfaces:
            print(colors.yellow + iface + colors.end)
        print("")

        # Interface input
        interface = input(colors.purple + "interface: " + colors.end)
        if interface not in valid_interfaces:
            print_error("Invalid interface selected.")
            return

        # Get IPv4 address of selected interface
        try:
            ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
        except (ValueError, KeyError, IndexError, TypeError):
            print_error("Invalid interface or no IPv4 assigned.")
            return

        ips = ip + "/24"
        print_info("scanning please wait...\n", start="\n")
        print(colors.blue + "MAC - IP" + colors.end)

        # Time tracking
        start_time = datetime.now()

        conf.verb = 0
        try:
            ans, unans = srp(
                Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ips),
                timeout=2,
                iface=interface,
                inter=0.1
            )
        except PermissionError:
            print_error('Root permissions required for packet sending.')
            return

        for snd, rcv in ans:
            print(rcv.sprintf(colors.yellow + "r%Ether.src% - %ARP.psrc%" + colors.end))

        stop_time = datetime.now()
        total_time = stop_time - start_time
        print_success("scan completed", start="\n")
        print_success("scan duration: " + str(total_time))

    except KeyboardInterrupt:
        print_info("network scanner terminated", start="\n")


# Run the scanner (optional - uncomment if running as script)
# if __name__ == "__main__":
#     scan()