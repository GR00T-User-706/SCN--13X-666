import argparse
import importlib
import os
import sys
import runpy
from pathlib import Path

# Dynamically resolve ROOT_DIR (GHOULNET_SANCTUARY)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Ensure ROOT_DIR is in sys.path for module imports
sys.path.append(str(ROOT_DIR))

# Rituals Directory Path (correctly alined
RITUALS_DIR = ROOT_DIR / 'rituals'

def list_rituals():
    rituals = []
    for file in os.listdir(RITUALS_DIR):
        if file.endswith('.py') and file != '__init__.py':
            rituals.append(file[:-3])  # Remove .py
    return rituals

def execute_ritual(ritual_name, args):
    ritual_file = RITUALS_DIR / f"{ritual_name}.py"
    if not ritual_file.exists():
        print(f"[-] Ritual '{ritual_file}' not fount.")
        return

# inject params as global variable temporarily
    for key, value in args.items():
        globals()[key] = value

# Execute the ritual script in an isolated namespace
    runpy.run_path(str(ritual_file), run_name="__main__")


def parse_args():
    parser = argparse.ArgumentParser(description='Lady LILITH - ShadowCore DaemonOps CLI')
    parser.add_argument('--list', action='store_true', help='List all available rituals')
    parser.add_argument('--run', metavar='RITUAL', help='Execute a specific ritual')
    parser.add_argument('--params', nargs='*', help='Parameters to pass to the ritual in key=value format')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()

    if args.list:
        rituals = list_rituals()
        print("[+] Available Rituals:")
        for r in rituals:
            print(f"    - {r}")
    elif args.run:
        param_dict = {}
        if args.params:
            for p in args.params:
                key, value = p.split('=')
                param_dict[key] = value
        execute_ritual(args.run, param_dict)
    else:
        print("[-] No action specified. Use --list or --run.")
