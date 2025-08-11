"""
CLI entry point and dispatcher for Shadowcore Nexus.
"""

import argparse

def main():
    parser = argparse.ArgumentParser(description="Shadowcore Nexus CLI")
    parser.add_argument("--mode", choices=["cli", "tui", "gui"], default="cli")
    args = parser.parse_args()
    if args.mode == "tui":
        from .tui import run_tui
        run_tui()
    else:
        print("Shadowcore Nexus CLI - Coming soon!")

if __name__ == "__main__":
    main()