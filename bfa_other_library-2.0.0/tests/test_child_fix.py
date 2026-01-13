#!/usr/bin/env python3
"""
Test script to verify the child addon import fix.
"""

import os
import sys
import tempfile
import shutil
import importlib

def create_test_structure():
    """Create a test child addon structure with relative imports."""
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp(prefix="bfa_test_child_")
    print(f"Created test directory: {temp_dir}")
    
    # Create child addon directory structure
    child_dir = os.path.join(temp_dir, "modular_child_addons")
    operators_dir = os.path.join(child_dir, "operators")
    
    os.makedirs(child_dir, exist_ok=True)
    os.makedirs(operators_dir, exist_ok=True)
    
    # Create __init__.py for child addon
    with open(os.path.join(child_dir, "__init__.py"), 'w') as f:
        f.write("""
# Child addon init
print("Child addon __init__.py loaded")
""")
    
    # Create operators/__init__.py
    with open(os.path.join(operators_dir, "__init__.py"), 'w') as f:
        f.write("""
# Operators package init
print("Operators __init__.py loaded")

def register():
    print("Operators registered")
    
def unregister():
    print("Operators unregistered")
""")
    
    # Create geometry_nodes.py in operators
    with open(os.path.join(operators_dir, "geometry_nodes.py"), 'w') as f:
        f.write("""
# Geometry nodes operators
print("Geometry nodes module loaded")

def register():
    print("Geometry nodes operators registered")
    
def unregister():
    print("Geometry nodes operators unregistered")

class EXAMPLE_OT_test_operator:
    bl_idname = "example.test_operator"
    bl_label = "Test Operator"
    
    def execute(self, context):
        print("Test operator executed")
        return {'FINISHED'}
""")
    
    # Create panels.py with relative import to operators
    with open(os.path.join(child_dir, "panels.py"), 'w') as f:
        f.write("""
# Panels module with relative import
print("Panels module loaded")

# This is the problematic relative import
from .operators.geometry_nodes import EXAMPLE_OT_test_operator

def register():
    print("Panels registered")
    # Normally would register the operator here
    
def unregister():
    print("Panels unregistered")
""")
    
    # Create wizards.py
    with open(os.path.join(child_dir, "wizards.py"), 'w') as f:
        f.write("""
# Wizards module
print("Wizards module loaded")

def register():
    print("Wizards registered")
    
def unregister():
    print("Wizards unregistered")
""")
    
    return temp_dir, child_dir

def test_import_logic():
    """Test the import logic that our fix uses."""
    print("\n" + "="*60)
    print("TESTING IMPORT LOGIC")
    print("="*60)
    
    temp_dir, child_dir = create_test_structure()
    
    try:
        # Test the logic from our fix
        parent_dir = os.path.dirname(child_dir)
        package_name = os.path.basename(child_dir)
        
        print(f"\nTest configuration:")
        print(f"  Parent directory: {parent_dir}")
        print(f"  Package name: {package_name}")
        print(f"  Child directory: {child_dir}")
        
        # Save original sys.path
        original_sys_path = sys.path.copy()
        
        try:
            # Add parent directory to sys.path (like our fix does)
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)
            
            print(f"\n1. Adding {parent_dir} to sys.path")
            print(f"   sys.path now starts with: {sys.path[0:2]}")
            
            # Now import the package
            print(f"\n2. Importing package: {package_name}")
            child_package = importlib.import_module(package_name)
            print(f"   ✓ Successfully imported package")
            
            # Import submodules
            print(f"\n3. Importing submodules:")
            
            # Test panels module (has relative import)
            try:
                full_name = f"{package_name}.panels"
                panels_module = importlib.import_module(full_name)
                print(f"   ✓ Successfully imported panels module")
            except ImportError as e:
                print(f"   ❌ Failed to import panels module: {e}")
                # Show what might be wrong
                print(f"   Looking for module at: {os.path.join(child_dir, 'panels.py')}")
                print(f"   File exists: {os.path.exists(os.path.join(child_dir, 'panels.py'))}")
            
            # Test operators subpackage
            try:
                operators_module = importlib.import_module(f"{package_name}.operators")
                print(f"   ✓ Successfully imported operators subpackage")
                
                # Test geometry_nodes submodule
                try:
                    geometry_nodes = importlib.import_module(f"{package_name}.operators.geometry_nodes")
                    print(f"   ✓ Successfully imported geometry_nodes module")
                except ImportError as e:
                    print(f"   ❌ Failed to import geometry_nodes: {e}")
                
            except ImportError as e:
                print(f"   ❌ Failed to import operators: {e}")
            
            # Test calling register functions
            print(f"\n4. Testing registration:")
            
            # Check if modules have register functions
            modules_to_check = [
                ("panels", panels_module if 'panels_module' in locals() else None),
                ("operators", operators_module if 'operators_module' in locals() else None),
            ]
            
            for name, module in modules_to_check:
                if module and hasattr(module, 'register'):
                    print(f"   ✓ {name} has register() function")
                    try:
                        module.register()
                        print(f"   ✓ Successfully called {name}.register()")
                    except Exception as e:
                        print(f"   ❌ Error calling {name}.register(): {e}")
                else:
                    print(f"   ⚠ {name} doesn't have register() function or module not loaded")
            
            print(f"\n✅ Import logic test completed!")
            
        finally:
            # Restore sys.path
            sys.path = original_sys_path
            
    finally:
        # Clean up
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up test directory: {temp_dir}")

def simulate_actual_issue():
    """Simulate the actual issue we're seeing in the logs."""
    print("\n" + "="*60)
    print("SIMULATING ACTUAL ISSUE")
    print("="*60)
    
    temp_dir, child_dir = create_test_structure()
    
    try:
        # Simulate the OLD broken approach (what we had before)
        print("\nSimulating OLD (broken) approach:")
        print("1. Changing to child directory and adding it to sys.path")
        
        original_cwd = os.getcwd()
        original_sys_path = sys.path.copy()
        
        try:
            os.chdir(child_dir)
            if child_dir not in sys.path:
                sys.path.insert(0, child_dir)
            
            print(f"   Current directory: {os.getcwd()}")
            print(f"   sys.path[0]: {sys.path[0]}")
            
            # Try to import panels directly (this will fail with relative import)
            print("\n2. Trying to import 'panels' directly:")
            try:
                # This simulates: module = __import__(module_name)
                module = __import__("panels")
                print("   ❌ UNEXPECTED: Import succeeded (it should fail)")
            except ImportError as e:
                print(f"   ✓ EXPECTED: Import failed with: {e}")
                
            print("\n3. Trying with importlib directly:")
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("panels", "panels.py")
                if spec:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules["panels"] = module
                    spec.loader.exec_module(module)
                    print("   ❌ UNEXPECTED: importlib succeeded")
                else:
                    print("   ✓ Could not create spec")
            except Exception as e:
                print(f"   ✓ EXPECTED: importlib failed with: {e}")
                
        finally:
            os.chdir(original_cwd)
            sys.path = original_sys_path
            
        print("\n✅ Simulation complete - the issue is confirmed!")
        
    finally:
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up test directory: {temp_dir}")

def main():
    print("Testing Child Addon Import Fix")
    print("="*60)
    
    test_import_logic()
    simulate_actual_issue()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("\nThe issue was:")
    print("1. Child addon modules use relative imports (e.g., 'from .operators.geometry_nodes import')")
    print("2. When loaded as top-level modules, Python doesn't know about the package structure")
    print("3. Relative imports fail with 'no known parent package'")
    
    print("\nThe solution (now implemented):")
    print("1. Add PARENT directory of child addon to sys.path")
    print("2. Import child addon as a package: importlib.import_module('modular_child_addons')")
    print("3. Import submodules as package.submodule: importlib.import_module('modular_child_addons.panels')")
    print("4. This makes relative imports work because Python sees the package structure")
    
    print("\nExpected result in Blender log:")
    print("  ✓ Loaded child addon package: modular_child_addons")
    print("  ✓ Loaded module: panels")
    print("  ✓ Loaded operators subpackage")
    print("  ✓ Registered modules...")
    print("  ✅ Child addon functionality loaded and registered")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()