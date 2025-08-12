"""import argparse
from .core.module_loader import ModuleLoader
from .core.path_resolver import PathResolver
from .interfaces.tui import DashboardTUI
from .utils.logging import configure_logging

def main():
    #Parse command line arguments
    parser = argparse.ArgumentParser(description="ShadowCore Nexus Dashboard")
    parser.add_argument("--cli", action="store_true", help="Use CLI interface")
    parser.add_argument("--gui", action="store_true", help="Use GUI interface")
    args = parser.parse_args()
    
    # Configure System
    path_resolver = PathResolver()
    configure_logging(path_resolver.resolve("logs"))

    # Initialize module ModuleLoader
    module_loader = ModuleLoader()
    module_dir=str(path_resolver.resolve("user_modules"))
    module_loader.discover_modules()
    
    # Launch appropriate interface
    if args.cli:
        from .interfaces.cli import DashboardCLI
        DashboardCLI(module_loader).run()
    else:
        DashboardTUI(module_loader).main()
        
if __name__ == "__main__":
    main()"""
#!/usr/bin/env python3
"""
Merged entry point for ShadowCore Nexus (SCN--13X-666)
- TUI-first minimal bootstrap from scaffold
- CLI/GUI toggle + logging + PathResolver from original
"""

import argparse
import sys
from pathlib import Path

# Local imports (adjust these paths when modules exist)
try:
    from .core.module_loader import ModuleLoader
except ImportError:
    # fallback to scaffold loader if core structure not yet in place
    from .module_loader import ModuleLoader

try:
    from .core.path_resolver import PathResolver
except ImportError:
    PathResolver = None

try:
    from .utils.logging import configure_logging
except ImportError:
    configure_logging = None

try:
    from .interfaces.tui import DashboardTUI
except ImportError:
    from .tui import run_tui as DashboardTUI

def main():
    parser = argparse.ArgumentParser(prog="shadowcore_nexus", description="ShadowCore Nexus Dashboard")
    parser.add_argument("--cli", action="store_true", help="Use CLI interface")
    parser.add_argument("--gui", action="store_true", help="Use GUI interface")
    parser.add_argument("--modules-dir", "-m", help="Modules directory (default depends on PathResolver or ./modules)")
    parser.add_argument("--no-watch", action="store_true", help="Disable filesystem watch (TUI)")
    parser.add_argument("--debug", action="store_true", help="Enable debug prints")
    args = parser.parse_args()

    # Resolve base paths
    if PathResolver:
        path_resolver = PathResolver()
        base_modules_dir = args.modules_dir or str(path_resolver.resolve("user_modules"))
    else:
        base_modules_dir = args.modules_dir or str(Path(__file__).resolve().parent / "modules")

    # Configure logging if available
    if configure_logging and PathResolver:
        configure_logging(path_resolver.resolve("logs"))

    # Initialize module loader
    loader = ModuleLoader(Path(base_modules_dir))
    loader.discover_all()

    # Launch appropriate interface
    if args.cli:
        try:
            from .interfaces.cli import DashboardCLI
            DashboardCLI(loader).run()
        except ImportError:
            print("[ERROR] CLI interface not found.")
            sys.exit(1)
    elif args.gui:
        try:
            from .interfaces.gui import DashboardGUI
            DashboardGUI(loader).run()
        except ImportError:
            print("[ERROR] GUI interface not found.")
            sys.exit(1)
    else:
        # Default to TUI (DashboardTUI can be scaffold's run_tui or your full TUI class)
        if callable(DashboardTUI):
            DashboardTUI(loader, watch=not args.no_watch, debug=args.debug)
        else:
            DashboardTUI(loader).main()

if __name__ == "__main__":
    main()
