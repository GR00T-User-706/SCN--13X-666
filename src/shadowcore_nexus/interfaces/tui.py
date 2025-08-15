import urwid
from pathlib import Path
from .core.module_loader import ModuleLoader
from .utils.logging import get_logger

logger = get_logger(__name__)

class ShadowCoreTUI:
    def __init__(self, modules_dir: Path, watch: bool = True, debug: bool = False):
        self.watch = watch
        self.debug = debug
        self.module_loader = ModuleLoader(modules_dir)
        self.module_loader.discover_all()

        self.palette = [
            ("header", "white", "dark blue"),
            ("footer", "white", "dark red"),
            ("button", "black", "light grey"),
            ("selected", "white", "dark green")
        ]
        self._build_ui()

    def _build_ui(self):
        """Build the TUI layout."""
        self.module_items = []
        modules = self.module_loader.get_list()  # [(key, name, entry), ...]

        if not modules:
            self.module_items.append(urwid.Text("No modules found in modules directory."))
        else:
            for key, display_name, entry in modules:
                btn = urwid.Button(display_name)
                urwid.connect_signal(btn, "click", self.run_module, key)
                self.module_items.append(urwid.AttrMap(btn, "button", "selected"))

        module_list = urwid.ListBox(urwid.SimpleFocusListWalker(self.module_items))
        header = urwid.AttrMap(urwid.Text("SCN Σ13X666 — ShadowCore Nexus", align="center"), "header")
        footer = urwid.AttrMap(urwid.Text("PID:SCN-Σ13X-666 | [F5] Reload | [F10] Exit"), "footer")

        self.frame = urwid.Frame(
            header=header,
            body=module_list,
            footer=footer
        )

    def run_module(self, button, module_key):
        """Run selected module."""
        entry = self.module_loader.get_entry(module_key)
        if not entry:
            logger.error(f"Module {module_key} not found in loader.")
            return
        try:
            run_func = entry.metadata.get("run")
            if callable(run_func):
                run_func()
            elif hasattr(entry.module, "main"):
                entry.module.main()
            else:
                logger.error(f"No callable entrypoint found for module {module_key}")
        except Exception as e:
            logger.error(f"Module {module_key} failed: {str(e)}")

    def reload_modules(self):
        """Reload module list."""
        self.module_loader.reload_if_changed()
        self._build_ui()

    def main(self):
        """Start the TUI main loop."""
        loop = urwid.MainLoop(self.frame, self.palette, unhandled_input=self.handle_keys)
        loop.run()

    def handle_keys(self, key):
        """Handle keyboard shortcuts."""
        if key.lower() == "f10":
            raise urwid.ExitMainLoop()
        elif key.lower() == "f5":
            self.reload_modules()
