"""
Module discovery and loading for Shadowcore Nexus.
Detects and imports new modules in the hub directory.
"""

import importlib.util
import os
import sys
from pathlib import Path
from ..utils.validation import validate_module_contract
from ..utils.logging import get_logger

logger = get_logger(__name__)

class ModuleLoader:
    def __init__(self, module_dir="modules"):
        self.module_dir = Path(module_dir)
        self.modules = {}
        self._create_module_dir()

    def _create_module_dir(self):
        '''Ensure module directory exists'''
        if not self.module_dir.exists():
            self.module_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created module directory: {self.module_dir}")
    

    def discover_modules(self):
        self.modules.clear()
        for file in self.module_dir.glob("*.py"):
            if file.name.startswith("_"):
                continue
            module_name = file.stem
            try:
                self.load_module(file, module_name)
            except Exception as e:
                logger.error(f"Faile to load {module_name}: {str(e)}")

    def load_module(self, file_path, module_name):
    # Load a single module with validation and correction
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec or not spec.loader:
            raise ImportError(f"Invalid module: {module_name}")
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)


        # Validate and correct module contract
        validate_module = validate_module_contract(module, module_name)

        self.modules[module_name] = {
            "module": validate_module,
            "path": file_path,
            "metadata": getattr(validate_module, "MODULE_META", {})
        }
        logger.info(f"Loaded module: {module_name}")

    """Retrieve loaded module by name"""
    def get_module(self, name):
        return self.modules.get(name, {}).get("module")
   
    """List all loaded modules with metadata"""
    def list_modules(self):
        return {name: data["metadata"] for name, data in self.modules.items()}


