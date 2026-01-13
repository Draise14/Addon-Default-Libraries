# Default Asset Library Addon Documentation

## 👀 Overview

This addon provides a comprehensive asset library system for Bforartists with smart primitives, wizard operations, and asset management capabilities. The addon is modular and designed for scalability.

This addon has been refactored into a modular architecture with two main components: Smart Primitives System and Wizard System


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


## Usage 🔧

### For End Users
- Enable the parent addon (e.g., "Default Asset Library Container")
- The functional addon ("Default Asset Library Functions") will be automatically installed and activated
- Use the functional addon as normal

### For Developers
1. **To create a new modular library addon**:
   - Copy this structure
   - Update `PARENT_ADDON_UNIQUE_ID` and `CHILD_ADDON_UNIQUE_ID` (optional) in parent `__init__.py`
   - Update blend files library folders in `CENTRAL_LIB_SUBFOLDERS`
   - Update child addon functionality as needed.

If you want to override the version of the addon with this one, then update CHILD_ADDON_UNIQUE_ID version.

2. **To add new functionality**:
   - Add to child addon files only
   - Parent addon only manages libraries and child addon lifecycle

## Technical Details ℹ️

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

## Troubleshooting

### Common Issues

1. **Panel not showing** - Check if `show_panel` is True and object has correct modifiers
2. **Handler not working** - Verify handler registration and message bus subscription
3. **Library not registered** - Check path existence and library registration logic

### Debugging

Enable console output to see handler messages and operation status.

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



## Module Structure 🛠️

### Core Modules

1. **`__init__.py`** - Main addon registration and library management
2. **`ops.py`** - Main operations hub and panel definitions
3. **`ui.py`** - User interface elements and menu integration
4. **`wizards.py`** - Wizard operations and automatic handlers
5. **`handlers_collections.py`** - Legacy collection handlers (migration recommended)

### Operators Module (`operators/`)

The operators are organized by node system type for better scalability:

1. **`geometry_nodes.py`** - Operations for Geometry Nodes assets
   - Smart primitive application
   - Panel control operations
   - Utility functions for Geometry Nodes

2. **`compositor.py`** - Operations for Compositor Nodes assets
   - Compositor setup application
   - Reset operations

3. **`shader.py`** - Operations for Shader Nodes assets
   - Shader setup application
   - Material creation

## Smart Primitives System 🔰

### Available Smart Primitives

The addon recognizes these Geometry Nodes-based smart primitives:
- Smart Capsule (and Revolved variants)
- Smart Circle (and Revolved variants) 
- Smart Cone (Rounded and Revolved variants)
- Smart Cube (Rounded variant)
- Smart Curve Lofted
- Smart Cylinder (Rounded Revolved variants)
- Smart Grid
- Smart Icosphere
- Smart Sphere (Revolved variant)
- Smart Spiral
- Smart Torus
- Smart Tube (Revolved and Rounded variants)

### Operations

1. **Apply Smart Primitives** (`object.apply_smart_primitives`)
   - Converts smart primitives to regular mesh objects
   - Options for joining and boolean operations
   - Robust error handling and state restoration

2. **Properties Panel** (`OBJECT_PT_geometry_nodes_panel`)
   - Dynamic UI that shows Geometry Nodes inputs
   - Organized by panels and sockets
   - Context-sensitive display

3. **Modifier Panel** (`OBJECT_PT_SmartPrimitiveModifierPanel`)
   - Shows apply operations in modifier properties
   - Always available when smart primitives are detected

## Wizard System 🧙

### Available Wizards

1. **Blend Normals by Proximity** (`wizard.blend_normals_by_proximity`)
   - Configures Geometry Nodes setup for normal blending
   - Automatic detection when assets are added
   - Collection selection and display options

### Handler Architecture

The wizard system uses a sophisticated handler architecture:

1. **Pre-import Handler** - Tracks collections before import
2. **Post-import Handler** - Detects new collections and invokes wizards
3. **Message Bus Subscription** - Listens for collection changes

## Asset Library Integration

### Supported Libraries

The addon automatically registers these asset libraries:
- Default Library (`Default Library/`)
- Geometry Nodes Library (`Geometry Nodes Library/`)
- Shader Nodes Library (`Shader Nodes Library/`)
- Compositor Nodes Library (`Compositor Nodes Library/`)

### Library Features

- Automatic registration on addon enable
- Proper path management
- Clean unregistration on disable

## User Interface 🎛️

### Menu Integration

The addon adds a "Smart Primitives" submenu to the Add menu (`VIEW3D_MT_add`) with icons for each primitive type.

### Panel Locations

1. **3D View Sidebar** (`VIEW_3D` → `UI` → `Item` category)
   - Primitive Properties panel for selected smart primitives

2. **Modifier Properties** (`PROPERTIES` → `WINDOW` → `Modifier` context)
   - Smart Primitive Operators panel

## Adding New Assets

### 1. Geometry Nodes Assets

To add new smart primitives:

1. Add the primitive name to `SMART_PRIMITIVE_NAMES` in `operators/geometry_nodes.py`
2. Ensure the Geometry Nodes group name starts with the primitive name
3. The system will automatically detect and handle the new primitive

### 2. Wizard Assets

To add new wizard operations:

1. Create a new operator class in `wizards.py`
2. Define asset recognition patterns
3. Add handler logic for automatic detection
4. Implement the wizard dialog and execution logic

### 3. Node Group Assets

For other node types (Compositor/Shader):

1. Add operations to the respective operator files
2. Implement asset detection logic if needed
3. Add UI elements as required

## Best Practices

### Code Organization

1. **Keep operations modular** - Separate by node system type
2. **Use descriptive class names** - Follow Blender naming conventions
3. **Implement proper error handling** - Use try-catch blocks and state restoration
4. **Add comprehensive documentation** - Document all classes and functions

### UI Design

1. **Context-sensitive panels** - Only show when relevant
2. **Clear labeling** - Use descriptive text and icons
3. **Consistent layout** - Follow Blender UI patterns
4. **Accessible operations** - Make common operations easily accessible

### Performance

1. **Efficient handlers** - Use message bus for efficient change detection
2. **Lazy evaluation** - Only process when necessary
3. **Cleanup operations** - Properly unregister and clean up resources


## Future Development 📅

1. **Version Management**: Better handling of parent/child version compatibility
2. **Auto-update**: Automatic updates of child addons
3. **Dependency Management**: Handling dependencies between modular addons

### Planned Features

1. **More wizard types** - Additional automatic operations for new assets
2. **Extended asset support** - More node system types and assets
3. **More asset related convenience operators** - Process multiple assets simultaneously with new functions
4. **Robust user exeperience** - Tested and reusable operation patterns

### Migration Path

The `handlers_collections.py` contains legacy code that should be migrated to the new wizard system for consistency.

## License

This addon is licensed under GPL v3. See the license block in each source file for details. This is indluded with Bforartists for free. 

## Support

For issues and feature requests, please use the GitHub tracker URL provided in the addon metadata.
