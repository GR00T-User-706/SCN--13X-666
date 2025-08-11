import argparse
import sys
from . import __package_name__, __version__
from .core import ShadowVeilCore

def launch_cli():
    parser = argparse.ArgumentParser(
        description=f'{__package_name__} - Cross-Platform Anti-Forensics Toolkit'
    )
    parser.add_argument('--mode', choices=['standard', 'stealth', 'paranoid'], 
                        default='standard', help='Operational mode')
    parser.add_argument('--encryption', choices=['low', 'medium', 'high'], 
                        default='high', help='Encryption strength')
    parser.add_argument('--execute', '-x', help='Command to execute stealthily')
    parser.add_argument('--tunnel', '-t', help='File to tunnel in filesystem')
    parser.add_argument('--covert', '-c', help='Data to send via covert channel')
    parser.add_argument('--clean', action='store_true', 
                        help='Activate cleanup protocol')
    
    args = parser.parse_args()
    
    sv = ShadowVeilCore(
        stealth_mode=args.mode,
        encryption_level=args.encryption
    )
    
    if sv.setup():
        print(f"[+] {__package_name__} v{__version__} activated")
        print(f"  ├─ OS: {platform.system()}")
        print(f"  ├─ Mode: {args.mode}")
        print(f"  └─ Encryption: {args.encryption}")
        
        if args.execute:
            pid = sv.execute_stealth(args.execute)
            print(f"  ├─ Executed stealth command (PID: {pid})")
        
        if args.tunnel:
            result = sv.tunnel_file(args.tunnel)
            print(f"  ├─ File tunneled to: {result}")
        
        if args.covert:
            if sv.covert_channel(args.covert.encode()):
                print("  ├─ Covert channel established")
        
        if args.clean:
            if sv.clean_system():
                print("  └─ System sanitized - exiting")
    else:
        print("[-] Initialization failed - aborting")
        sys.exit(1)