# Modular Asset Library Architecture

## Overview

This addon has been refactored into a modular architecture with two main components:

1. **Parent Addon (Library Manager)**: Manages asset library registration and tracking
2. **Child Addon (Functional Addon)**: Contains all operators, panels, handlers, and wizards

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│          PARENT ADDON (Library Manager)     │
│  • Registers asset libraries                │
│  • Tracks library usage                     │
│  • Manages child addon installation         │
│  • No functional UI/operators               │
└─────────────────┬───────────────────────────┘
                  │
                  │ Copies & Activates
                  ▼
┌─────────────────────────────────────────────┐
│          CHILD ADDON (Functional Addon)     │
│  • All operators (geometry nodes, shaders)  │
│  • All UI panels                            │
│  • Wizards and handlers                     │
│  • Menu entries                             │
└─────────────────────────────────────────────┘
```

## How It Works

### Parent Addon Responsibilities
1. **Library Management**: Registers asset libraries in user preferences
2. **Asset Tracking**: Tracks which addons are using which libraries
3. **Child Addon Management**: 
   - Copies child addon files to user preferences
   - Activates the child addon
   - Ensures child addon is properly installed and active
4. **Cleanup**: Properly removes libraries when no longer needed

### Child Addon Responsibilities
1. **Functionality**: All the actual addon functionality
2. **UI**: All panels, menus, and interface elements
3. **Wizards**: Interactive setup wizards for assets
4. **Operators**: All Blender operators for asset manipulation

## Benefits

1. **Modularity**: Can have multiple parent addons managing different asset libraries
2. **Single Registration**: Functionality (operators, panels) only registered once via child addon
3. **Clean Separation**: Library management separate from functionality
4. **Easy Updates**: Update libraries independently of functionality
5. **Better User Experience**: Users only see functional addons in their addon list

## Files Structure

### Parent Addon Files
- `__init__.py` - Main parent addon entry point
- `utility.py` - Utility functions for library and child addon management
- `blender_manifest.toml` - Addon manifest
- `operators/` - Empty directory (functionality moved to child addon)
- `panels.py`, `ui.py`, `wizards.py`, etc. - Empty files

### Child Addon Files (in `child_addon/` directory)
- `__init__.py` - Child addon entry point
- `operators/` - All operator classes
- `panels.py` - UI panels
- `ui.py` - Menu entries and UI extensions
- `wizards.py` - Wizard system
- `wizard_handlers.py` - Wizard detection handlers
- `wizard_operators.py` - Wizard operator classes
- `ops.py` - Main operations module

## Installation Process

1. User enables parent addon
2. Parent addon:
   - Registers asset libraries in preferences
   - Copies child addon files to user preferences
   - Activates child addon
3. Child addon registers all functionality
4. User sees functional addon in their addon list

## Usage

### For End Users
- Enable the parent addon (e.g., "Default Asset Library Container")
- The functional addon ("Default Asset Library Functions") will be automatically installed and activated
- Use the functional addon as normal

### For Developers
1. **To create a new modular library addon**:
   - Copy this structure
   - Update `PARENT_ADDON_UNIQUE_ID` and `CHILD_ADDON_UNIQUE_ID` in parent `__init__.py`
   - Update library folders in `CENTRAL_LIB_SUBFOLDERS`
   - Update child addon functionality as needed

2. **To add new functionality**:
   - Add to child addon files only
   - Parent addon only manages libraries and child addon lifecycle

## Technical Details

### Child Addon Installation Path
Child addons are installed to: `{USER_PREFS}/addons/modular_child_addons/`

### Library Tracking
- Uses JSON tracking files in central library directory
- Tracks which parent addons are using which libraries
- Prevents cleanup of libraries still in use

### Error Handling
- Robust error handling in both parent and child addons
- Graceful degradation if child addon installation fails
- Automatic retry of failed operations

## Testing

To test the modular architecture:

1. Enable the parent addon in Blender
2. Check that:
   - Asset libraries appear in preferences
   - Child addon is installed and activated
   - All functionality works (operators, panels, wizards)
3. Disable parent addon
4. Verify child addon is deactivated
5. Re-enable parent addon
6. Verify everything works again

## Troubleshooting

### Child Addon Not Appearing
1. Check user preferences addons list for "Default Asset Library Functions"
2. Check console for installation errors
3. Verify file permissions in user preferences directory

### Libraries Not Appearing
1. Check Blender preferences → File Paths → Asset Libraries
2. Verify central library directory exists and is writable
3. Check console for library registration errors

### Functionality Not Working
1. Ensure child addon is active in preferences
2. Check that required Python modules are available
3. Verify asset library paths are correct

## Future Enhancements

1. **Multiple Child Addons**: Support for multiple functional addons from single parent
2. **Version Management**: Better handling of parent/child version compatibility
3. **Auto-update**: Automatic updates of child addons
4. **Dependency Management**: Handling dependencies between modular addons

## License

Same as main addon license (GPL v3).