from pathlib import Path
import importlib.util
import sys
import traceback
from typing import Dict, Optional
from ..utils.validation import validate_module_contract
from ..utils.logging import get_logger

logger = get_logger(__name__)

class ModuleEntry:
    def __init__(self, path: Path):
        self.path = path
        self.key = path.stem
        self.module = None
        self.metadata = {}
        self.mtime = 0

    def load(self):
        """Load a single module, validate it, and capture metadata."""
        try:
            spec_name = self.key
            spec = importlib.util.spec_from_file_location(spec_name, str(self.path))
            if not spec or not spec.loader:
                raise ImportError(f"Invalid module: {spec_name}")

            mod = importlib.util.module_from_spec(spec)
            sys.modules[spec_name] = mod
            spec.loader.exec_module(mod)  # type: ignore

            # Validate module structure
            mod = validate_module_contract(mod, spec_name)

            # Prefer MODULE_META, else try register()
            if hasattr(mod, "MODULE_META"):
                self.metadata = getattr(mod, "MODULE_META", {}) or {}
            elif hasattr(mod, "register") and callable(mod.register):
                self.metadata = mod.register() or {}
            elif hasattr(mod, "main") and callable(mod.main):
                self.metadata = {"name": self.key, "run": getattr(mod, "main")}

            self.module = mod
            self.mtime = self.path.stat().st_mtime
            logger.info(f"Loaded module: {self.key}")
            return True
        except Exception as e:
            logger.error(f"Failed to load {self.key}: {e}")
            traceback.print_exc()
            return False

class ModuleLoader:
    def __init__(self, modules_dir: Path = Path("modules")):
        self.modules_dir = Path(modules_dir)
        self.modules_dir.mkdir(parents=True, exist_ok=True)
        self.entries: Dict[str, ModuleEntry] = {}

    def discover_all(self):
        """Load all modules in the directory."""
        for p in sorted(self.modules_dir.glob("*.py")):
            if p.name.startswith("_"):
                continue
            key = p.stem
            if key not in self.entries:
                self.entries[key] = ModuleEntry(p)
            self.entries[key].load()

        # Prune removed
        to_remove = [k for k, e in self.entries.items() if not e.path.exists()]
        for k in to_remove:
            self.entries.pop(k, None)

    def get_list(self):
        """Return list of (key, display_name, entry) tuples."""
        return [(k, e.metadata.get("name", k), e) for k, e in self.entries.items()]

    def reload_if_changed(self):
        """Reload modules if file timestamps changed, detect new ones."""
        changed = False
        for k, e in list(self.entries.items()):
            try:
                mtime = e.path.stat().st_mtime
                if mtime != e.mtime:
                    logger.info(f"Reloading module: {k}")
                    e.load()
                    changed = True
            except FileNotFoundError:
                logger.warning(f"Module removed: {k}")
                self.entries.pop(k, None)
                changed = True

        # Detect new files
        for p in self.modules_dir.glob("*.py"):
            if p.stem not in self.entries and not p.name.startswith("_"):
                self.entries[p.stem] = ModuleEntry(p)
                self.entries[p.stem].load()
                changed = True

        return changed

    def get_entry(self, key) -> Optional[ModuleEntry]:
        """Retrieve ModuleEntry by key."""
        return self.entries.get(key)
