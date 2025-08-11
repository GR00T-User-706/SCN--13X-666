import os
import sys
import platform

__package_name__ = "ShadowVeil"
__version__ = "3.0.0"
__module_type__ = "security/anti-forensics"
__compatibility__ = ["TUI", "GUI", "CLI"]
__author__ = "BlackOps Division"
__description__ = "Cross-platform anti-forensics module"
__exported_methods__ = [
    "execute_stealth",
    "tunnel_file",
    "camouflage_traffic",
    "covert_channel",
    "clean_system"
]

HUB_REGISTRY = {}

def register_with_hub(hub_instance):
    HUB_REGISTRY[hub_instance.hub_id] = {
        'instance': hub_instance,
        'status': 'active'
    }
    hub_instance.register_module(
        module_name=__package_name__,
        module_version=__version__,
        module_type=__module_type__,
        activation_callback=activate_in_hub
    )

def activate_in_hub(hub_instance, config=None):
    from .core import ShadowVeilCore
    
    hub_config = config or hub_instance.get_module_config(__package_name__)
    stealth_mode = hub_config.get('stealth_mode', 'standard')
    encryption_level = hub_config.get('encryption', 'high')
    
    sv = ShadowVeilCore(
        stealth_mode=stealth_mode,
        encryption_level=encryption_level
    )
    
    if sv.setup():
        hub_instance.log(f"{__package_name__} activated in {stealth_mode} mode")
        return sv
    hub_instance.error(f"{__package_name__} initialization failed")
    return None

def detect_hub_environment():
    return 'CYBER_DASHBOARD_HUB' in os.environ

if detect_hub_environment():
    try:
        from .hub_adapter import ShadowVeilHubAdapter
        hub_id = os.environ['CYBER_DASHBOARD_HUB']
        register_with_hub(ShadowVeilHubAdapter(hub_id))
    except ImportError:
        pass

def main():
    from .cli import launch_cli
    launch_cli()

if __name__ == "__main__":
    main()