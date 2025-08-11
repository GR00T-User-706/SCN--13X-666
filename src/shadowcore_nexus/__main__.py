import argparse
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
    main()