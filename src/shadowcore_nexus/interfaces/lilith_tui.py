import sys
from pathlib import Path
# === Absolute Path Override ===
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path = [str(ROOT_DIR)] + sys.path  # Force ShadowCore to be sys.path[0]
from daemon_logger import start_watcher
import os
import termios
import tty
import importlib
import importlib.util
from core.paths import RITUALS_DIR, ensure_directories
from colorama import Fore, Style
from colorama import init as colorama_init
#============================================================================#
# Force ANSI colors on Windows and others
os.environ['PYTHONLEGACYWINDOWSSTDOUT'] = '1'  # Windows workaround
os.environ['TERM'] = 'xterm-256color'          # Force xterm term type
#============================================================================#
colorama_init(autoreset=True)
#============================================================================#
def list_rituals():
    rituals = []
    for file in os.listdir(RITUALS_DIR):
        if file.endswith('.py') and file != '__init__.py':
            rituals.append(file[:-3])
    return rituals
#============================================================================#
def execute_ritual(ritual_name, params=None):
    try:
        # Resolve the full file path to the Ritual .py file
        ritual_file = RITUALS_DIR / f"{ritual_name}.py"
        if not ritual_file.exists():
            print(f"[-] Ritual file {ritual_file} not found")
            return

        # Dynamically load the Ritual Python file directly from path
        spec = importlib.util.spec_from_file_location(f"rituals.{ritual_name}", ritual_file)
        ritual = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ritual)

        # Get Ritual Parameters
        if hasattr(ritual, 'PARAMS'):
            param_prompts = ritual.PARAMS
        else:
            param_prompts = []

        # Prompt for parameters if not provided
        if params is None:
            params = {}
            for prompt in param_prompts:
                value = input(f"{prompt}: ")
                params[prompt] = value

        # Execute Ritual's run() method
        if hasattr(ritual, 'run'):
            ritual.run(**params)
        else:
            print(f"[-] Ritual '{ritual_name}' missing 'run' method.")

    except Exception as e:
        print(f"[-] Error executing ritual '{ritual_name}': {e}")
#============================================================================#

def get_single_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

#============================================================================#

def main_menu():
    while True:
        print(f"\n{Fore.RED}--- Lady LILITH TUI Control Panel ---{Style.RESET_ALL}")
        rituals = list_rituals()
        for idx, ritual in enumerate(rituals, 1):
            print(f"{Fore.LIGHTRED_EX}{idx}. {ritual}{Style.RESET_ALL}", flush=True)
        print(f"{Fore.LIGHTRED_EX}0. Exit{Style.RESET_ALL}", flush=True)

        print(f"{Fore.YELLOW}Select a Ritual by pressing its number key:{Style.RESET_ALL} ", end='', flush=True)
        choice = get_single_key()
        print(choice)    # Echo the key pressed

#        choice = input(f"{Fore.YELLOW}Select a Ritual to execute: {Style.RESET_ALL}")
        if choice == '0':
            print(f"{Fore.GREEN}[*] Exiting LILITH Control Panel.{Style.RESET_ALL}")
            break
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(rituals):
            print(f"{Fore.RED}[-] Invalid selection.{Style.RESET_ALL}")
            continue

        ritual_name = rituals[int(choice)-1]
        print(f"{Fore.GREEN}[+] Selected Ritual: {ritual_name}{Style.RESET_ALL}")
        
        execute_ritual(ritual_name)
 
if __name__ == '__main__':
    ensure_directories()  # Ensure structure exists
    start_watcher()       # Activate Watcher Feed
    main_menu()           # Launch LILITH TUI
# v2.5
#============================================================================#

#============================================================================#
#v1.1 ritual execution function
#not working for network mapping module
#============================================================================#
#def execute_ritual(ritual_name, params=None):
#    try:
#        module_path = f'rituals.{ritual_name}'
#        ritual = importlib.import_module(module_path)
#        if hasattr(ritual, 'PARAMS'):
#            param_prompts = ritual.PARAMS
#        else:
#            param_prompts = []
#        if params is None:
#            params = {}
#            for prompt in param_prompts:
#                value = input(f"{prompt}: ")
#                params[prompt] = value 
#        if hasattr(ritual, 'run'):
#            ritual.run(**params)
#        else:
#            print(f"[-] Ritual '{ritual_name}' missing 'run 'method.")
#    except ModuleNotFoundError:
#        print(f"[-] Ritual '{ritual_name}' not found.")
#    except Exception as e:
#        print(f"[-] Error executing ritual '{ritual_name}': {e}")