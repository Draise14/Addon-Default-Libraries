# Default Asset Library Addon Documentation

## Overview

This addon provides a comprehensive asset library system for Bforartists with smart primitives, wizard operations, and asset management capabilities. The addon is modular and designed for scalability.

## Module Structure

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

## Smart Primitives System

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

## Wizard System

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

## User Interface

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

## Troubleshooting

### Common Issues

1. **Panel not showing** - Check if `show_panel` is True and object has correct modifiers
2. **Handler not working** - Verify handler registration and message bus subscription
3. **Library not registered** - Check path existence and library registration logic

### Debugging

Enable console output to see handler messages and operation status.

## Future Development

### Planned Features

1. **More wizard types** - Additional automatic operations
2. **Extended asset support** - More node system types
3. **Batch operations** - Process multiple assets simultaneously
4. **Template system** - Reusable operation patterns

### Migration Path

The `handlers_collections.py` contains legacy code that should be migrated to the new wizard system for consistency.

## License

This addon is licensed under GPL v3. See the license block in each source file for details. This is indluced with Bforartists for free. 


## Support

For issues and feature requests, please use the GitHub tracker URL provided in the addon metadata.
