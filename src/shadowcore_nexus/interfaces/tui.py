import urwid
from ..core.module_loader import ModuleLoader
from ..utils.logging import get_logger

logger = get_logger(__name__)

class DashboardTUI:
    def __init__(self,module_loader):
        self.module_loader = module_loader
        self.palette = [
            ("header", "white", "dark blue")
            ("footer", "white", "dark red")
            ("button", "black", "light grey")
            ("selected", "white", "dark green")
        ]
        self._build_ui()
        
    def _build_ui(self):
        """Build TUI components"""
        # Module  list
        modules = self.module_loader.list_modules()
        self.module_item = []
        
        for name, meta in modules.items():
            btn = urwid.Button(meta.get("name", name))
            urwid.connect_signal(btn, "click", self.run_module, name)
            self.module_items.append(urwid.AttrMap(btn, "button", "selected"))
            
        module_list = urwid.ListBox(urwid.SimpleFocusListWalker(self.module_items))
        
        # Header amd footer
        header = urwid.AttrMap(urwid.Text("SHADOWCORE NEXUS", align="center"), "header")
        
        footer = urwid.AttrMap(urwid.Text("PID:SCN-Σ13X-666 | [F1] Help [F10] Exit"), "footer")
        
        # Layout
        self.frame = urwid.Frame(
            header=header,
            body=module_list,
            footer=footer
        )
        
    def run_module(self, button, module_name):
        """Execute selected module"""
        module = self.module_loader.get_module(module_name)
        if module:
            try:
                module.initialize()
            except Exception as e:
                logger.error(f"Module {module_name} failed: {str(e)}")
                
    def main(self):
        """Start TUI main loop"""
        loop = urwid.MainLoop(self.frame, self.palette, unhandled_input=self.handle_keys)
        loop.run()
    
    def handle_keys(self, key):
        """Handle global keyboard shortcuts"""
        if key == "f10":
            raise urwid.ExitMainLoop()                                