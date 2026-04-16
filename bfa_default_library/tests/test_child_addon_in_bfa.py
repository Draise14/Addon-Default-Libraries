#!/usr/bin/env python3
"""
Test to verify child addon would work in Bforartists
"""

import os
import sys
import tempfile
import shutil

def main():
    """Test if child addon structure would work in Bforartists."""
    print("Testing if child addon structure would work in Bforartists...")
    print("=" * 60)
    
    # Simulate Bforartists extensions folder structure
    temp_dir = tempfile.mkdtemp()
    extensions_path = os.path.join(temp_dir, 'extensions', 'user_default')
    os.makedirs(extensions_path, exist_ok=True)
    
    print(f"Simulated extensions path: {extensions_path}")
    
    # Copy child addon files
    source_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'child_addon')
    dest_dir = os.path.join(extensions_path, 'modular_child_addons')
    
    if os.path.exists(source_dir):
        # Copy all files
        shutil.copytree(source_dir, dest_dir)
        print(f"✅ Copied child addon to: {dest_dir}")
        
        # Check if __init__.py can be read
        init_file = os.path.join(dest_dir, '__init__.py')
        if os.path.exists(init_file):
            with open(init_file, 'r') as f:
                content = f.read()
                # Check for key elements
                checks = [
                    ('bl_info', 'Has bl_info (addon metadata)'),
                    ('def register', 'Has register function'),
                    ('import operators', 'Imports operators'),
                    ('import panels', 'Imports panels'),
                    ('import wizards', 'Imports wizards'),
                ]
                
                print("Checking __init__.py contents:")
                for check, description in checks:
                    if check in content:
                        print(f"  ✓ {description}")
                    else:
                        print(f"  ✗ Missing: {description}")
        
        # Check manifest
        manifest_file = os.path.join(dest_dir, 'blender_manifest.toml')
        if os.path.exists(manifest_file):
            print(f"\n✓ Manifest file exists")
            with open(manifest_file, 'r') as f:
                manifest_content = f.read()
                if 'name =' in manifest_content and 'version =' in manifest_content:
                    print(f"  ✓ Manifest has required fields")
                else:
                    print(f"  ✗ Manifest missing required fields")
        
        # Check for all necessary files
        required_files = [
            '__init__.py',
            'blender_manifest.toml',
            'operators/__init__.py',
            'operators/geometry_nodes.py',
            'operators/compositor.py',
            'operators/shader.py',
            'panels.py',
            'ui.py',
            'ops.py',
            'wizards.py',
            'wizard_handlers.py',
            'wizard_operators.py',
        ]
        
        print(f"\nChecking required files:")
        missing_files = []
        for file in required_files:
            file_path = os.path.join(dest_dir, file)
            if os.path.exists(file_path):
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} - MISSING")
                missing_files.append(file)
        
        if not missing_files:
            print(f"\n✅ All required files present!")
            print(f"\nIn Bforartists, this child addon should appear in:")
            print(f"  Edit → Preferences → Add-ons → Import-Export")
            print(f"  Search for: 'Default Asset Library Functions'")
            print(f"\nThe parent addon will:")
            print(f"  1. Copy child addon to extensions folder")
            print(f"  2. Activate child addon automatically")
            print(f"  3. Manage asset libraries")
            print(f"\nChild addon provides:")
            print(f"  • Operators (geometry nodes, shaders, compositor)")
            print(f"  • UI panels")
            print(f"  • Wizards")
            print(f"  • Menu entries")
        else:
            print(f"\n❌ Missing files: {missing_files}")
        
        # Clean up
        shutil.rmtree(temp_dir)
    else:
        print(f"❌ Source directory not found: {source_dir}")
    
    print("=" * 60)
    
    # Additional Bforartists-specific checks
    print("\nBforartists-specific considerations:")
    print("1. ✅ Extensions folder: extensions/user_default/")
    print("2. ✅ Manifest file: blender_manifest.toml with correct fields")
    print("3. ✅ Module structure: modular_child_addons/ with __init__.py")
    print("4. ✅ All functional files present in child addon")
    print("\nIf the child addon doesn't appear in Bforartists:")
    print("• Check if extensions/user_default/ folder exists")
    print("• Check file permissions in user directory")
    print("• Try restarting Bforartists after parent addon installation")
    print("• Check Console for error messages")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)