#!/usr/bin/env python3
"""
Static analysis of the modular addon logic.
"""

import os
import sys
import ast
import json

def analyze_file(filepath):
    """Analyze a Python file for potential issues."""
    print(f"\n=== Analyzing {os.path.basename(filepath)} ===")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for common issues
    issues = []
    
    # Check for missing imports (basic check)
    if 'json.load(' in content or 'json.dump(' in content:
        if 'import json' not in content:
            issues.append("Missing 'import json'")
    
    # Check for duplicate imports
    lines = content.split('\n')
    imports = [line for line in lines if line.strip().startswith('import ') or line.strip().startswith('from ')]
    import_set = set()
    for imp in imports:
        if imp in import_set:
            issues.append(f"Duplicate import: {imp}")
        import_set.add(imp)
    
    # Check configuration values
    if filepath.endswith('__init__.py'):
        # Check for required configuration variables
        required_vars = [
            'PARENT_ADDON_UNIQUE_ID',
            'PARENT_ADDON_DISPLAY_NAME', 
            'PARENT_ADDON_VERSION',
            'CHILD_ADDON_UNIQUE_ID',
            'CHILD_ADDON_DISPLAY_NAME',
            'CHILD_ADDON_VERSION',
            'CENTRAL_LIB_SUBFOLDERS',
            'CHILD_ADDON_MODULES'
        ]
        
        for var in required_vars:
            if f'{var} =' not in content and f'{var}=' not in content:
                issues.append(f"Missing required configuration: {var}")
    
    if issues:
        print("⚠ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✓ No obvious issues found")
    
    return issues

def check_directory_structure(base_dir):
    """Check if the directory structure matches expectations."""
    print("\n=== Directory Structure Check ===")
    
    expected_dirs = [
        'Default Library',
        'Geometry Nodes Library', 
        'Shader Nodes Library',
        'Compositor Nodes Library',
        'child_addon',
        'operators',
        'tests'
    ]
    
    for dir_name in expected_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"✓ {dir_name}: exists")
            
            # Check if library directories have blend files
            if 'Library' in dir_name:
                blend_files = [f for f in os.listdir(dir_path) if f.endswith('.blend')]
                if blend_files:
                    print(f"  - Contains {len(blend_files)} .blend file(s)")
                else:
                    print(f"  ⚠ No .blend files found in {dir_name}")
        else:
            print(f"⚠ {dir_name}: missing")

def analyze_logic_flow():
    """Analyze the logical flow based on code reading."""
    print("\n=== Logic Flow Analysis ===")
    
    print("\n1. Registration Flow:")
    print("   - When addon registers:")
    print("     a. Adds parent to child addon tracking")
    print("     b. Registers libraries (copies files, adds to preferences)")
    print("     c. Ensures child addon files are installed")
    print("     d. Loads child addon functionality if not already loaded")
    
    print("\n2. Multiple Addon Handling:")
    print("   - Each addon has unique PARENT_ADDON_UNIQUE_ID")
    print("   - Central library tracks which addons are using it")
    print("   - Child addon functionality is shared (only loaded once)")
    print("   - Child addon tracking tracks which parents are using it")
    
    print("\n3. Unregistration Flow:")
    print("   - When addon unregisters:")
    print("     a. Removes parent from child addon tracking")
    print("     b. Checks if other parents are still active")
    print("     c. If no other parents, unloads child addon functionality")
    print("     d. Removes addon from central library tracking")
    print("     e. If no addons left using central library, cleans up files")
    
    print("\n4. Potential Issues to Check:")
    print("   - Ensure child addon files are only removed when truly unused")
    print("   - Make sure central library registration persists when addons unregister")
    print("   - Handle edge cases when Blender preferences can't be accessed")
    print("   - Ensure unique IDs are actually unique across different addon copies")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=== Modular Addon Architecture Analysis ===")
    
    # Analyze main files
    main_files = [
        '__init__.py',
        'utility.py',
        'child_addon/__init__.py'
    ]
    
    all_issues = []
    for filepath in main_files:
        full_path = os.path.join(base_dir, filepath)
        if os.path.exists(full_path):
            issues = analyze_file(full_path)
            all_issues.extend(issues)
        else:
            print(f"\n⚠ File not found: {filepath}")
    
    # Check directory structure
    check_directory_structure(base_dir)
    
    # Analyze logic flow
    analyze_logic_flow()
    
    # Check for actual blend files in library directories
    print("\n=== Library Content Check ===")
    library_dirs = [d for d in os.listdir(base_dir) if 'Library' in d and os.path.isdir(os.path.join(base_dir, d))]
    for lib_dir in library_dirs:
        lib_path = os.path.join(base_dir, lib_dir)
        files = os.listdir(lib_path)
        blend_files = [f for f in files if f.endswith('.blend')]
        cats_files = [f for f in files if f.endswith('.cats.txt')]
        
        print(f"\n{lib_dir}:")
        print(f"  - Total files: {len(files)}")
        print(f"  - .blend files: {len(blend_files)}")
        print(f"  - .cats.txt files: {len(cats_files)}")
        
        if len(blend_files) == 0:
            print("  ⚠ WARNING: No .blend files found!")
    
    # Summary
    print("\n=== Analysis Summary ===")
    if all_issues:
        print(f"Found {len(all_issues)} issue(s) that should be fixed:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print("✓ No critical issues found in static analysis")
    
    print("\n=== Recommendations ===")
    print("1. Ensure PARENT_ADDON_UNIQUE_ID is truly unique for each addon copy")
    print("2. Test the addon with multiple instances to verify tracking works")
    print("3. Consider adding more error handling for file operations")
    print("4. Document the process for creating new modular addons from this template")

if __name__ == '__main__':
    main()