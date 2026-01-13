# Changelog

All notable changes to the BFA Default Asset Library addon will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- **Modular UI refactor**: Moved preferences panel (`LIBADDON_APT_preferences`) and library management operators (`LIBADDON_OT_cleanup_libraries`, `LIBADDON_OT_readd_libraries`) from `__init__.py` to dedicated `ui.py` module for better code organization and maintainability.

### Fixed
- **Child addon import issues**: Fixed `"attempted relative import with no known parent package"` error by loading child addon as proper Python package using `importlib.import_module()` instead of standalone modules
- **JSON decode errors**: Added specific `json.JSONDecodeError` handling for malformed tracking files
- **Directory creation**: Added `os.makedirs()` before writing tracking files to prevent write errors
- **Duplicate imports**: Removed duplicate `import sys` in `load_child_addon_functionality()`
- **Bug fix**: Added missing `sys` import at module level in `utility.py` (was causing potential NameError on fallback path resolution)
- **Bug fix**: Removed duplicate handler cleanup in `panels.py` unregister function
- **Multi-parent duplicate prevention**: Added registration tracking flags to prevent duplicate menu entries, scene properties, and handlers when multiple parent addons are active:
  - `child_addon/ui.py`: Menu functions now only register once via `_menu_registered` flag
  - `child_addon/ops.py`: Scene properties tracked via `_scene_props_registered` flag
  - `child_addon/wizard_handlers.py`: Scene properties moved from module level to `register()` function with tracking flag

### Removed (Dead Code Cleanup)
- **Parent addon stub files**: Removed 9 unused stub files that were never imported:
  - Root level: `ops.py`, `panels.py`, `wizards.py`, `wizard_handlers.py`, `wizard_operators.py`
  - `operators/` directory: `__init__.py`, `geometry_nodes.py`, `compositor.py`, `shader.py`
- **`__init__.py`**: Removed unused fallback functions `_load_child_addon_modules_individually()` and `_load_operator_modules_individually()` (~110 lines)
- **`utility.py`**: Removed unused manifest functions (`create_child_addon_manifest`, `read_child_addon_manifest`, `remove_child_addon_manifest`, `get_child_addons_by_parent`) and unused library check functions (`is_central_library_registered`, `get_central_library_index`) (~100 lines)
- **`child_addon/ui.py`**: Removed broken/dead code including `get_asset_library_path()`, `append_asset_as_object()`, `WM_OT_AppendAsset` operator, `ASSET_MT_primitive_add` menu, `primitive_menu_func()`, and `SMART_PRIMITIVE_ASSETS` list (~80 lines)
- **`child_addon/wizard_handlers.py`**: Removed unused import `wizard_operators as wiz_ops`
- **Redundant documentation**: Consolidated `MODULAR_ARCHITECTURE_SUMMARY.md` and `FIXES_SUMMARY.md` into CHANGELOG and MODULAR_ARCHITECTURE.md

### Improved (Code Consolidation)
- **Centralized module constants**: Created `CHILD_ADDON_SUBMODULES` and `CHILD_ADDON_ALL_MODULES` constants in `__init__.py` to replace 5+ hardcoded module lists
- **Consolidated path resolution**: Refactored `utility.py` to use single internal `_get_user_resource_path()` function, reducing ~90 lines of duplicate code to ~50 lines
- **Added utility functions**: Added `is_bforartists()` and `get_icon()` utility functions to `child_addon/__init__.py` for consistent Bforartists vs Blender detection
- **Unloading improvements**: Updated to search for both package-style (`modular_child_addons.panels`) and underscore-style (`modular_child_addons_panels`) module names

### Added
- **`.gitignore`**: Added proper gitignore for `__pycache__/`, `*.pyc`, `*.zip`, IDE files, and OS files

### File Changes Summary
- `__init__.py`: Reduced from ~1124 lines to ~1000 lines
- `utility.py`: Reduced from ~560 lines to ~420 lines
- `child_addon/ui.py`: Reduced from ~340 lines to ~255 lines
- `child_addon/__init__.py`: Added shared utility functions
- `child_addon/wizard_handlers.py`: Removed unused import
- `child_addon/panels.py`: Fixed duplicate handler cleanup
- Removed 9 stub files (~280 lines total)
- Removed 2 redundant documentation files

## [1.2.7] - Previous Release

### Features
- Modular parent/child addon architecture
- Central asset library system with smart tracking
- Automatic child addon functionality loading
- Multi-parent addon support with shared child functionality
- Library management operators in preferences panel
