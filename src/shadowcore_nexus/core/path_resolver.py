from pathlib import Path
import sys
import platform
from ..utils.compat import get_data_dir

class PathResolver
    def __init__(self):
        self.system = platform.system()
        self._init_paths()
        
    def _init_paths(self):
        """Initialize OS-appropriate paths"""
        self.base_dir = Path(__file__).parent.parent.resolve()
        
        # OS-specific data directories
        self.data_dir = get_data_dir("shadowcore_nexus")
        
        # Module directories
        self.core_modules = self.base_dir / "core_modules"
        self.user_modules = self.data_dir / "modules"
        
        # Create required directories
        self.user_modules.mkdir(parents=True, exist_ok=True)
        
    def resolve(self, path_type):
        """Resolve paths by type"""
        paths = {
            "base": self.base_dir,
            "config": self.data_dir / "config",
            "logs": self.data_dir / "logs",
            "cache": self.data_dir /"cache",
            "core_modules": self.core_modules,
            "user_modules": self.user_modules,
            "artifacts": self.data_dir / "artifacts"
        }
        return paths.get(path_type, self.base_dir)