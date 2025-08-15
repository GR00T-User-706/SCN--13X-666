#!/usr/bin/env python3
"""
Entry point for ShadowCore Nexus (SCN--13X-666)
Unified TUI-first launcher.
"""

import argparse
import sys
from pathlib import Path

try:
    from .core.module_loader import ModuleLoader
except ImportError:
    from .module_loader import ModuleLoader

try:
    from .interfaces.tui import ShadowCoreTUI
except ImportError:
    print("[ERROR] TUI interface not found.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(prog="shadowcore_nexus", description="ShadowCore Nexus Dashboard")
    parser.add_argument("--modules-dir", "-m", help="Modules directory (default: ./modules)")
    parser.add_argument("--no-watch", action="store_true", help="Disable module hot reload")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    modules_dir = Path(args.modules_dir or Path(__file__).resolve().parent / "modules")

    tui = ShadowCoreTUI(modules_dir, watch=not args.no_watch, debug=args.debug)
    tui.main()

if __name__ == "__main__":
    main()
