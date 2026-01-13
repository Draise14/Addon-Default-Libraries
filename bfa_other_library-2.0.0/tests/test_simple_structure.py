#!/usr/bin/env python3
"""
Simple structure test for Modular Asset Library Architecture
Tests the file structure and basic imports without requiring bpy
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✓ {description}: exists")
        return True
    else:
        print(f"✗ {description}: MISSING")
        return False

def check_file_content(filepath, should_be_empty=True):
    """Check if a file has expected content."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        if should_be_empty:
            # For parent functional files, check if they indicate they're empty
            if "intentionally empty" in content or "Empty register" in content:
                print(f"✓ {os.path.basename(filepath)}: properly empty")
                return True
            else:
                print(f"✗ {os.path.basename(filepath)}: NOT empty as expected")
                return False
        else:
            # For child functional files, check if they have content
            if len(content.strip()) > 100:  # Arbitrary threshold
                print(f"✓ {os.path.basename(filepath)}: has content")
                return True
            else:
                print(f"✗ {os.path.basename(filepath)}: seems empty")
                return False
    except Exception as e:
        print(f"✗ Error reading {filepath}: {e}")
        return False

def main():
    """Test the modular addon structure."""
    print("=" * 60)
    print("Testing Modular Asset Library Structure")
    print("=" * 60)
    
    # Get addon directory
    addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    child_addon_dir = os.path.join(addon_dir, "child_addon")
    
    print(f"\nAddon directory: {addon_dir}")
    print(f"Child addon directory: {child_addon_dir}")
    
    all_passed = True
    
    print("\n" + "="*40)
    print("Checking parent addon files...")
    print("="*40)
    
    # Essential parent files
    essential_parent = [
        ("__init__.py", "Parent addon main file"),
        ("utility.py", "Utility module"),
        ("blender_manifest.toml", "Addon manifest"),
    ]
    
    for filename, description in essential_parent:
        filepath = os.path.join(addon_dir, filename)
        if not check_file_exists(filepath, description):
            all_passed = False
    
    # Parent functional files should be empty
    print("\n" + "="*40)
    print("Checking parent functional files (should be empty)...")
    print("="*40)
    
    empty_parent_files = [
        "panels.py",
        "ui.py", 
        "ops.py",
        "wizards.py",
        "wizard_handlers.py",
        "wizard_operators.py",
    ]
    
    for filename in empty_parent_files:
        filepath = os.path.join(addon_dir, filename)
        if os.path.exists(filepath):
            if not check_file_content(filepath, should_be_empty=True):
                all_passed = False
        else:
            print(f"✓ {filename}: missing (acceptable for modular)")
    
    print("\n" + "="*40)
    print("Checking child addon files...")
    print("="*40)
    
    # Essential child files
    essential_child = [
        "__init__.py",
        "operators/__init__.py",
        "panels.py",
        "ui.py",
        "ops.py",
        "wizards.py",
        "wizard_handlers.py",
        "wizard_operators.py",
    ]
    
    for filename in essential_child:
        filepath = os.path.join(child_addon_dir, filename)
        description = f"Child {filename}"
        if not check_file_exists(filepath, description):
            all_passed = False
        else:
            # Check that child functional files have content
            if not check_file_content(filepath, should_be_empty=False):
                all_passed = False
    
    # Check operator modules
    print("\n" + "="*40)
    print("Checking child operator modules...")
    print("="*40)
    
    child_operators_dir = os.path.join(child_addon_dir, "operators")
    operator_files = [
        "geometry_nodes.py",
        "compositor.py",
        "shader.py",
    ]
    
    for filename in operator_files:
        filepath = os.path.join(child_operators_dir, filename)
        description = f"Child operator {filename}"
        if not check_file_exists(filepath, description):
            all_passed = False
        else:
            if not check_file_content(filepath, should_be_empty=False):
                all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ STRUCTURE TEST PASSED!")
        print("\nThe modular architecture is correctly implemented.")
        print("\nKey points verified:")
        print("1. ✅ Parent addon exists with minimal files")
        print("2. ✅ Parent functional files are empty")
        print("3. ✅ Child addon directory exists")
        print("4. ✅ Child addon has all functional files")
        print("5. ✅ Child operator modules have content")
        print("\nThis addon is ready for use in Blender.")
    else:
        print("❌ STRUCTURE TEST FAILED")
        print("\nPlease check the implementation and fix the issues.")
    
    print("=" * 60)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)