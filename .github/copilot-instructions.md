# Copilot Instructions for SCN--13X-666 (Shadowcore Nexus)

## Project Overview
- **Shadowcore Nexus** is a modular, OS-independent Python dashboard hub for rapid deployment and management of Python modules ("Rituals").
- Supports TUI, GUI, and CLI interfaces. Modules are auto-discovered and managed dynamically.
- Major components: `core/` (module management, config, daemon ops), `interfaces/` (CLI, TUI, logging), `utils/` (validation, logging), `modules/` (plug-in modules), `rituals/` (specialized modules), and `artifacts/` (configs, logs, outputs).

## Architecture & Patterns
- **Plug-in System:** Modules are Python scripts in `modules/` with a `main()` function and `MODULE_META` metadata. The loader (`core/module_loader.py`) auto-discovers, validates, and loads them.
- **UI Abstraction:** Multiple UIs (CLI, TUI, GUI) are implemented in `interfaces/`. Each UI interacts with the core via a dispatcher pattern.
- **Artifacts & Logging:** All runtime artifacts, logs, and outputs are stored in `artifacts/` subfolders. Logging is centralized via `utils/logging.py`.
- **Validation:** Module contracts are enforced using `utils/validation.py`.

## Developer Workflows
- **Run the Hub:**
  - From the `src/` directory, launch the main entry: `python -m shadowcore_nexus` or use the appropriate UI script in `interfaces/`.
- **Add a Module:**
  - Drop a Python file in `modules/` with a `main()` and `MODULE_META` dict.
  - The loader will auto-discover and validate it on next run.
- **Testing:**
  - Place tests in `test/`. Use `pytest` or `python -m unittest discover test`.
- **Debugging:**
  - Use the logging system (`get_logger`) for debug output. Logs are in `artifacts/logs/`.

## Conventions & Integration
- **Module Contract:** Each module must define `main()` and `MODULE_META`.
- **Relative Imports:** Use relative imports within the package. Run scripts as modules (e.g., `python -m shadowcore_nexus.core.module_loader`).
- **External Dependencies:** Some modules require extra packages (see their `requirements.txt`). Install with `pip install -r modules/<mod>/requirements.txt`.
- **Sensitive Operations:** Anti-forensics and stealth features (e.g., in `modules/shadowveil/`) are for research/defense only.

## Examples
- See `modules/shadowveil/README.md` and `modules/net_mapper/README.md` for module-specific usage and integration.
- Example module loader usage: `ModuleLoader(module_dir="shadowcore_nexus/modules").discover_modules()`

## Key Files & Directories
- `core/module_loader.py`: Module discovery/validation/loader logic
- `interfaces/cli.py`, `interfaces/tui.py`: UI entrypoints
- `utils/validation.py`, `utils/logging.py`: Core utilities
- `modules/`, `rituals/`: Drop-in modules
- `artifacts/`: Configs, logs, outputs

---
For more, see the main `README.md` and module READMEs. When in doubt, follow the patterns in `core/` and `interfaces/`.
