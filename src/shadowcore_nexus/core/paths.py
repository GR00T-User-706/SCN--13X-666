# What This Does:
# Resolves absolute paths dynamically — never hardcodes.
# Ensures all critical folders exist — builds them on-the-fly if missing.
# Any script can now import:
# from core.paths import LOGS_DIR, OUTPUTS_DIR
# This eliminates all your broken path issues across scripts.

from pathlib import Path

# Root Directory (ShadowCore)
ROOT_DIR = Path(__file__).resolve().parent.parent

# Tier 1 Directories
CORE_DIR = ROOT_DIR / 'core'
ARTIFACTS_DIR = ROOT_DIR / 'artifacts'
RITUALS_DIR = ROOT_DIR / 'rituals'
OPS_DIR = ROOT_DIR / 'ops'
UI_DIR = ROOT_DIR / 'ui'

# Artifacts Subdirectories
LOGS_DIR = ARTIFACTS_DIR / 'logs'
OUTPUTS_DIR = ARTIFACTS_DIR / 'outputs'
CONFIGS_DIR = ARTIFACTS_DIR / 'configs'
KEYS_DIR = ARTIFACTS_DIR / 'keys'

# Rituals Subdirectories
RITUALS_MODULES_DIR = RITUALS_DIR / 'modules'


# Modules Subdirectories
NET_MAPPER_DIR = RITUALS_MODULES_DIR / 'net_mapper'
GHOULNET_WARFRAME = RITUALS_MODULES_DIR / 'ghoulnet warframe'
PHANTOM_SCRY_DIR = RITUALS_MODULES_DIR / 'phantom scry'

# Phantom Scry Subdirectories
CORE_SUB_DIR = PHANTOM_SCRY_DIR / 'Phantom_scry/core'
MODULES_SUB_DIR = PHANTOM_SCRY_DIR / 'Phantom_scry/modules'
RITUALS_SUB_DIR = PHANTOM_SCRY_DIR / 'Phantom_scry/rituals'
ARTIFACTS_SUB_DIR = PHANTOM_SCRY_DIR / 'Phantom_scry/artifacts'


# UI Subdirectories
UI_COMPONENTS_DIR = UI_DIR / 'components'

# Ensure all critical directories exist
def ensure_directories():
    dirs = [
        ARTIFACTS_DIR, LOGS_DIR, OUTPUTS_DIR, CONFIGS_DIR, KEYS_DIR,
        RITUALS_MODULES_DIR, UI_COMPONENTS_DIR
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

# Execute on import
ensure_directories()

# Optional: Debug Print (Remove in production)
if __name__ == "__main__":
    print(f"ROOT_DIR: {ROOT_DIR}")
    print(f"Artifacts Path: {ARTIFACTS_DIR}")
    print(f"Rituals Path: {RITUALS_DIR}")
    print(f"Logs Path: {LOGS_DIR}")
