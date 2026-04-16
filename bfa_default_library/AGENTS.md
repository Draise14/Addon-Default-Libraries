# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Blender/Bforartists addon implementing a **modular parent/child architecture** for asset library management. Multiple parent addons can share a single child addon containing operators, panels, and wizards.

## Architecture

```
Parent Addon (Library Manager)          Child Addon (Shared Functionality)
├── __init__.py - Core logic            ├── operators/ - Node operators
├── ui.py - Preferences panel           ├── panels.py - UI panels
├── utility.py - Path/tracking utils    ├── wizards.py - Asset wizards
└── Asset Libraries (copied to central) └── wizard_*.py - Wizard handlers
```

**Key Concept**: Parent addon manages libraries and lifecycle. Child addon is copied to user extensions folder and loaded dynamically. Multiple parents share one child instance.

## Configuration (in `__init__.py`)

Each addon instance requires unique identifiers:
```python
PARENT_ADDON_UNIQUE_ID = "default_asset_library_1_2_7"  # MUST BE UNIQUE
PARENT_ADDON_DISPLAY_NAME = "Default Asset Library"
PARENT_ADDON_VERSION = (1, 2, 7)
CENTRAL_LIB_SUBFOLDERS = ["Default Library", "Geometry Nodes Library", ...]
```

## Registration Flow

1. `register()` called → registers UI module → starts delayed timer (0.5s)
2. `delayed_setup()` runs → copies libraries to central location → installs child addon files → loads child functionality
3. Child addon loaded as package via `importlib.import_module("modular_child_addons")`
4. Tracking updated in `child_addon_tracking.json`

## Multi-Parent Behavior

- First parent: Creates central library, loads child addon
- Additional parents: Join tracking, reuse loaded child
- Parent unregisters: Removes from tracking, keeps child if others active
- Last parent unregisters: Unloads child, cleans up libraries

## Tracking Files (in central library folder)

- `.addon_tracking.json` - Which addons contribute which library files
- `child_addon_tracking.json` - Active parents list, functionality loaded state

## Running Tests

```bash
cd bfa_default_library/tests
python test_modular_architecture.py   # Architecture verification
python test_central_library.py        # Multi-addon scenarios
python test_file_copying.py           # File operations
```

## Key Functions

| Function | Location | Purpose |
|----------|----------|---------|
| `load_child_addon_functionality()` | `__init__.py` | Dynamically imports and registers child modules |
| `get_central_library_path()` | `utility.py` | Returns platform-specific central library path |
| `add_addon_to_central_library()` | `utility.py` | Registers addon, copies assets, updates tracking |
| `get_child_addon_tracking_data()` | `__init__.py` | Reads multi-parent tracking JSON |

## Important Patterns

**Module Loading**: Child addon must be loaded as a package (not individual files) to enable relative imports:
```python
sys.path.insert(0, parent_dir)
child_package = importlib.import_module("modular_child_addons")
module = importlib.import_module("modular_child_addons.panels")
```

**Multi-Parent Check**: Always verify before cleanup:
```python
if len(tracking_data["active_parents"]) == 0:
    unload_child_addon_functionality(force=True)
```

**Error Recovery**: Handle missing directories and malformed JSON gracefully - return defaults rather than crash.

## File Responsibilities

- `__init__.py` (~1124 lines): Library registration, child addon lifecycle, delayed setup
- `utility.py` (~561 lines): Path resolution, file copying, addon tracking
- `ui.py` (~170 lines): Preferences panel, library management operators
- `child_addon/operators/__init__.py`: Operator registration for geometry/shader/compositor

## Blender API Notes

- Use `bpy.app.timers.register()` for delayed initialization (avoids preferences access during load)
- `AddonPreferences.bl_idname` must match package name (`__package__`)
- Check `"already registered"` errors when registering classes (addon may be reloaded)
