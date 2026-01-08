#!/usr/bin/env python3
"""
Verify all fixes for the modular addon architecture.
"""

import os
import re

def verify_fixes():
    print("=" * 60)
    print("VERIFYING MODULAR ADDON FIXES")
    print("=" * 60)
    
    # Read the __init__.py file
    with open(__file__.replace('verify_fixes.py', '__init__.py'), 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track issues
    issues = []
    successes = []
    
    print("\n=== Fix Verification ===")
    
    # Check 1: json import exists
    if 'import json' in content:
        successes.append("json import found")
    else:
        issues.append("Missing 'import json'")
    
    # Check 2: Directory creation in save_child_addon_tracking_data
    if 'os.makedirs(central_base, exist_ok=True)' in content:
        successes.append("Directory creation in save_child_addon_tracking_data")
    else:
        issues.append("Missing directory creation in save_child_addon_tracking_data")
    
    # Check 3: Directory check in get_child_addon_tracking_data
    if 'p.exists(central_base) and p.exists(tracking_file)' in content:
        successes.append("Directory check in get_child_addon_tracking_data")
    else:
        issues.append("Missing directory check in get_child_addon_tracking_data")
    
    # Check 4: JSON decode error handling
    if 'json.JSONDecodeError' in content:
        successes.append("JSON decode error handling added")
    else:
        issues.append("Missing JSON decode error handling")
    
    # Check 5: No duplicate 'import sys' in load_child_addon_functionality
    load_start = content.find('def load_child_addon_functionality():')
    load_end = content.find('def unload_child_addon_functionality')
    if load_start != -1:
        load_section = content[load_start:load_end]
        import_count = load_section.count('import sys')
        if import_count <= 1:
            successes.append(f"Proper sys imports in load_child_addon_functionality ({import_count})")
        else:
            issues.append(f"Duplicate sys imports in load_child_addon_functionality ({import_count})")
    else:
        issues.append("Cannot find load_child_addon_functionality function")
    
    print("\n=== Configuration Verification ===")
    
    # Find versions using simple string matching
    parent_version = None
    child_version = None
    bl_version = None
    
    # Find PARENT_ADDON_VERSION
    match = re.search(r'PARENT_ADDON_VERSION\s*=\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
    if match:
        parent_version = tuple(map(int, match.groups()))
        successes.append(f"PARENT_ADDON_VERSION: {parent_version}")
    else:
        issues.append("Cannot find PARENT_ADDON_VERSION")
    
    # Find CHILD_ADDON_VERSION
    match = re.search(r'CHILD_ADDON_VERSION\s*=\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
    if match:
        child_version = tuple(map(int, match.groups()))
        successes.append(f"CHILD_ADDON_VERSION: {child_version}")
    else:
        issues.append("Cannot find CHILD_ADDON_VERSION")
    
    # Find bl_info version - handle different quote styles
    patterns = [
        r'"version"\\s*:\\s*\\((\\d+),\\s*(\\d+),\\s*(\\d+)\\)',  # double quotes
        r"'version'\\s*:\\s*\\((\\d+),\\s*(\\d+),\\s*(\\d+)\\)",  # single quotes
        r'\"version\"\\s*:\\s*\\((\\d+),\\s*(\\d+),\\s*(\\d+)\\)',  # escaped double quotes
    ]
    
    match = None
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            break
    if match:
        bl_version = tuple(map(int, match.groups()))
        successes.append(f"bl_info version: {bl_version}")
    else:
        issues.append("Cannot find bl_info version")
    
    # Check version consistency
    if parent_version and child_version and bl_version:
        if parent_version == child_version == bl_version:
            successes.append("All versions match!")
        else:
            issues.append(f"Version mismatch! Parent: {parent_version}, Child: {child_version}, bl_info: {bl_version}")
    
    print("\n=== Key Functions Verification ===")
    
    # Check for required functions
    required_functions = [
        ('register', 'Main registration'),
        ('unregister', 'Main unregistration'),
        ('register_library', 'Library registration'),
        ('load_child_addon_functionality', 'Load child addon'),
        ('unload_child_addon_functionality', 'Unload child addon'),
        ('add_parent_to_child_tracking', 'Track parent registration'),
        ('remove_parent_from_child_tracking', 'Track parent unregistration'),
        ('should_keep_child_addon_active', 'Check child addon status'),
        ('get_child_addon_tracking_data', 'Get tracking data'),
        ('save_child_addon_tracking_data', 'Save tracking data'),
    ]
    
    for func_name, description in required_functions:
        if f'def {func_name}' in content:
            successes.append(f"{func_name}: {description}")
        else:
            issues.append(f"Missing function: {func_name}")
    
    print("\n=== Results ===")
    
    if successes:
        print(f"\n✅ {len(successes)} checks passed:")
        for success in successes[:10]:  # Show first 10
            print(f"  ✓ {success}")
        if len(successes) > 10:
            print(f"  ... and {len(successes) - 10} more")
    
    if issues:
        print(f"\n❌ {len(issues)} issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ All checks passed!")
    
    print("\n=== Architecture Summary ===")
    print("The modular addon architecture implements:")
    print("1. Central library management with tracking")
    print("2. Child addon sharing across multiple parent addons")
    print("3. Proper cleanup when last parent unregisters")
    print("4. Error handling for file operations and JSON parsing")
    
    print("\n=== Testing Recommendations ===")
    print("1. Install the addon in Blender and verify:")
    print("   - Libraries appear in Asset Browser")
    print("   - Child addon functionality loads")
    print("2. Install a second modular addon (with different unique IDs)")
    print("   - Verify child addon is not reloaded")
    print("3. Uninstall one addon:")
    print("   - Verify child addon stays active")
    print("4. Uninstall the last addon:")
    print("   - Verify child addon unloads")
    print("   - Verify libraries are cleaned up")
    
    print("\n" + "=" * 60)
    
    return len(issues) == 0

if __name__ == "__main__":
    success = verify_fixes()
    exit(0 if success else 1)