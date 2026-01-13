#!/usr/bin/env python3
"""
Test the actual file structure and paths for the modular addon
"""

import os
import sys

def print_system_info():
    """Print information about the current system and paths."""
    print("System Information:")
    print(f"  Platform: {sys.platform}")
    print(f"  Python: {sys.version}")
    print(f"  Current directory: {os.getcwd()}")
    print()

def check_addon_structure():
    """Check the modular addon structure."""
    addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Addon directory: {addon_dir}")
    print()
    
    # Check parent addon files
    print("Parent Addon Structure:")
    parent_files = [
        ("__init__.py", "Main parent addon file"),
        ("utility.py", "Utility module"),
        ("blender_manifest.toml", "Addon manifest"),
        ("panels.py", "Parent panels (should be empty)"),
        ("ui.py", "Parent UI (should be empty)"),
        ("ops.py", "Parent ops (should be empty)"),
        ("wizards.py", "Parent wizards (should be empty)"),
        ("wizard_handlers.py", "Parent wizard handlers (should be empty)"),
        ("wizard_operators.py", "Parent wizard operators (should be empty)"),
    ]
    
    for filename, description in parent_files:
        filepath = os.path.join(addon_dir, filename)
        exists = os.path.exists(filepath)
        status = "✓" if exists else "✗"
        print(f"  {status} {filename}: {description}")
        if exists:
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    if "intentionally empty" in content or "Empty register" in content:
                        print(f"    ↳ Correctly empty")
                    elif len(content.strip()) > 100:
                        print(f"    ↳ Has content ({len(content)} chars)")
                    else:
                        print(f"    ↳ Minimal content")
            except:
                print(f"    ↳ Could not read file")
    
    print()
    
    # Check child addon directory
    child_addon_dir = os.path.join(addon_dir, "child_addon")
    print(f"Child Addon Directory: {child_addon_dir}")
    if os.path.exists(child_addon_dir):
        print(f"  ✓ Child addon directory exists")
        
        # Check child addon structure
        child_files = [
            "__init__.py",
            "operators/__init__.py",
            "operators/geometry_nodes.py",
            "operators/compositor.py",
            "operators/shader.py",
            "panels.py",
            "ui.py",
            "ops.py",
            "wizards.py",
            "wizard_handlers.py",
            "wizard_operators.py",
        ]
        
        print("  Child Addon Files:")
        for filename in child_files:
            filepath = os.path.join(child_addon_dir, filename)
            exists = os.path.exists(filepath)
            status = "✓" if exists else "✗"
            print(f"    {status} {filename}")
            if exists:
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        if "bl_info" in content:
                            print(f"      ↳ Has bl_info (addon metadata)")
                        if "def register" in content:
                            print(f"      ↳ Has register function")
                except:
                    print(f"      ↳ Could not read file")
    else:
        print(f"  ✗ Child addon directory missing!")
    
    print()
    
    # Check library directories
    print("Library Directories:")
    library_dirs = [
        "Default Library",
        "Geometry Nodes Library",
        "Shader Nodes Library",
        "Compositor Nodes Library"
    ]
    
    for dirname in library_dirs:
        dirpath = os.path.join(addon_dir, dirname)
        exists = os.path.exists(dirpath)
        status = "✓" if exists else "✗"
        print(f"  {status} {dirname}")
        if exists:
            # Count blend files
            blend_files = [f for f in os.listdir(dirpath) if f.endswith('.blend')]
            print(f"    ↳ Contains {len(blend_files)} .blend files")

def check_imports():
    """Check if modules can be imported."""
    print("Import Tests:")
    
    addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, addon_dir)
    
    modules_to_test = [
        ("utility", "Utility module"),
    ]
    
    for module_name, description in modules_to_test:
        try:
            module = __import__(module_name)
            print(f"  ✓ {module_name}: {description}")
            # Check some key functions
            if module_name == "utility":
                functions = [
                    "get_central_library_path",
                    "get_user_preferences_path",
                    "get_bfa_extensions_path",
                    "get_child_addon_path"
                ]
                for func in functions:
                    if hasattr(module, func):
                        print(f"    ↳ Has {func}()")
                    else:
                        print(f"    ↳ Missing {func}()")
        except ImportError as e:
            print(f"  ✗ {module_name}: {e}")

def check_child_addon_import():
    """Try to import child addon modules."""
    print("\nChild Addon Import Tests:")
    
    addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    child_addon_dir = os.path.join(addon_dir, "child_addon")
    
    if os.path.exists(child_addon_dir):
        sys.path.insert(0, child_addon_dir)
        
        # Try to read and parse the __init__.py
        init_file = os.path.join(child_addon_dir, "__init__.py")
        try:
            with open(init_file, 'r') as f:
                content = f.read()
                if "bl_info" in content:
                    print(f"  ✓ Child __init__.py has bl_info")
                else:
                    print(f"  ✗ Child __init__.py missing bl_info")
                
                # Check imports
                imports_found = []
                if "import operators" in content:
                    imports_found.append("operators")
                if "import panels" in content:
                    imports_found.append("panels")
                if "import wizards" in content:
                    imports_found.append("wizards")
                if "import wizard_handlers" in content:
                    imports_found.append("wizard_handlers")
                if "import wizard_operators" in content:
                    imports_found.append("wizard_operators")
                if "import ops" in content:
                    imports_found.append("ops")
                if "import ui" in content:
                    imports_found.append("ui")
                
                if imports_found:
                    print(f"  ✓ Child __init__.py imports: {', '.join(imports_found)}")
                else:
                    print(f"  ✗ Child __init__.py has no imports")
                    
        except Exception as e:
            print(f"  ✗ Error reading child __init__.py: {e}")
    else:
        print(f"  ✗ Child addon directory not found")

def main():
    """Run all tests."""
    print("=" * 80)
    print("MODULAR ASSET LIBRARY ADDON - STRUCTURE VALIDATION")
    print("=" * 80)
    print()
    
    print_system_info()
    check_addon_structure()
    check_imports()
    check_child_addon_import()
    
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print("The modular addon architecture should have:")
    print("1. ✅ Parent addon with minimal files (most functionality files are empty)")
    print("2. ✅ Child addon directory with all functional modules")
    print("3. ✅ Library directories with .blend files")
    print("4. ✅ Utility module with BFA path functions")
    print("5. ✅ Child addon with proper bl_info and imports")
    print()
    print("To use in Blender/Bforartists:")
    print("1. Install the parent addon")
    print("2. Parent will copy child addon to: USER/extensions/user_default/modular_child_addons/")
    print("3. Parent will attempt to activate the child addon")
    print("4. Child addon provides all UI/operators/wizards")
    print("5. Parent manages libraries and child addon lifecycle")
    print("=" * 80)

if __name__ == "__main__":
    main()