import sys
from pathlib import Path

# === Absolute Path Override ===
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path = [str(ROOT_DIR)] + sys.path  # Force ShadowCore to be sys.path[0

from core.config import config
from core.paths import RITUALS_DIR
import importlib

# Ensure ShadowCore is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


class DaemonHandler:
    def __init__(self):
        self.modules = {}

    def load_module(self, module_name):
        try:
            module_path = f'rituals.{module_name}'
            module = importlib.import_module(module_path)
            self.modules[module_name] = module
            print(f"[+] Loaded module: {module_name}")
        except ModuleNotFoundError:
            print(f"[-] Failed to load module: {module_name}")

    def initialize_modules(self):
        for module_name in config.get("modules_enabled", []):
            self.load_module(module_name)

    def execute_module(self, module_name, *args, **kwargs):
        module = self.modules.get(module_name)
        if module and hasattr(module, 'run'):
            print(f"[>] Executing module: {module_name}")
            module.run(*args, **kwargs)
        else:
            print(f"[-] Module not found or 'run' method missing: {module_name}")

# For testing only
if __name__ == "__main__":
    daemon = DaemonHandler()
    daemon.initialize_modules()
    daemon.execute_module('encoding', 'test_input.txt')
