#!/usr/bin/env python3
"""
Test script for Modular Asset Library Architecture
Tests the parent-child addon system and library management
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utility

def test_utility_functions():
    """Test utility module functions."""
    print("Testing utility functions...")
    
    # Test get_central_library_path
    central_path = utility.get_central_library_path()
    print(f"✓ Central library path: {central_path}")
    
    # Test get_user_preferences_path
    user_prefs_path = utility.get_user_preferences_path()
    print(f"✓ User preferences path: {user_prefs_path}")
    
    # Test get_bforartists_user_preferences_folder
    bfa_prefs_path = utility.get_bforartists_user_preferences_folder()
    print(f"✓ Bforartists prefs path: {bfa_prefs_path}")
    
    print("✅ Utility functions test passed")
    return True

def test_child_addon_management():
    """Test child addon management functions."""
    print("\nTesting child addon management...")
    
    # Create a test parent addon info
    parent_addon_info = {
        'name': 'Test Parent Addon',
        'version': (1, 0, 0),
        'unique_id': 'test_parent_addon_1_0_0'
    }
    
    # Test get_addon_identifier
    addon_id = utility.get_addon_identifier(parent_addon_info)
    print(f"✓ Addon identifier: {addon_id}")
    
    # Test child addon status functions
    is_installed, is_active, addon_path = utility.get_child_addon_status("test_child")
    print(f"✓ Child addon status - Installed: {is_installed}, Active: {is_active}")
    
    # Test manifest creation
    try:
        manifest_file = utility.create_child_addon_manifest("test_child", parent_addon_info)
        print(f"✓ Manifest created: {manifest_file}")
        
        # Test manifest reading
        manifest_data = utility.read_child_addon_manifest("test_child")
        if manifest_data:
            print(f"✓ Manifest read successfully")
        else:
            print(f"✗ Failed to read manifest")
            return False
            
        # Test getting child addons by parent
        child_addons = utility.get_child_addons_by_parent(addon_id)
        print(f"✓ Child addons for parent: {child_addons}")
        
        # Test manifest removal
        if utility.remove_child_addon_manifest("test_child"):
            print(f"✓ Manifest removed successfully")
        else:
            print(f"✗ Failed to remove manifest")
            return False
            
    except Exception as e:
        print(f"✗ Manifest tests failed: {e}")
        return False
    
    print("✅ Child addon management tests passed")
    return True

def test_library_tracking():
    """Test library tracking functions."""
    print("\nTesting library tracking...")
    
    # Create a test central library directory
    with tempfile.TemporaryDirectory() as temp_dir:
        central_base = os.path.join(temp_dir, "asset_libraries")
        os.makedirs(central_base, exist_ok=True)
        
        # Override get_central_library_path for testing
        original_get_path = utility.get_central_library_path
        utility.get_central_library_path = lambda: central_base
        
        try:
            # Create test addon info
            test_addon_info = {
                'name': 'Test Library Addon',
                'version': (2, 0, 0),
                'unique_id': 'test_library_addon_2_0_0'
            }
            
            # Test adding addon to tracking
            test_libraries = ["Test Library 1", "Test Library 2"]
            test_addon_dir = temp_dir
            
            utility.add_addon_to_central_library(
                test_addon_info, 
                test_libraries, 
                test_addon_dir, 
                central_base
            )
            print(f"✓ Addon added to central library tracking")
            
            # Test reading tracking data
            tracking_data = utility.read_addon_tracking(central_base)
            if tracking_data:
                print(f"✓ Tracking data read: {len(tracking_data)} addon(s)")
            else:
                print(f"✗ Failed to read tracking data")
                return False
                
            # Test getting active addons count
            active_count = utility.get_active_addons_count(central_base)
            print(f"✓ Active addons count: {active_count}")
            
            # Test removing addon from tracking
            utility.remove_addon_from_central_library(
                test_addon_info, 
                central_base, 
                cleanup_mode='check'
            )
            print(f"✓ Addon removed from tracking")
            
        finally:
            # Restore original function
            utility.get_central_library_path = original_get_path
    
    print("✅ Library tracking tests passed")
    return True

def test_file_structure():
    """Test that the addon has the correct modular structure."""
    print("\nTesting file structure...")
    
    addon_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check parent addon files
    required_parent_files = [
        "__init__.py",
        "utility.py",
        "blender_manifest.toml",
    ]
    
    for file in required_parent_files:
        file_path = os.path.join(addon_dir, file)
        if os.path.exists(file_path):
            print(f"✓ Parent file exists: {file}")
        else:
            print(f"✗ Missing parent file: {file}")
            return False
    
    # Check child addon directory
    child_addon_dir = os.path.join(addon_dir, "child_addon")
    if os.path.exists(child_addon_dir):
        print(f"✓ Child addon directory exists")
    else:
        print(f"✗ Missing child addon directory")
        return False
    
    # Check child addon files
    required_child_files = [
        "__init__.py",
        "operators/__init__.py",
        "panels.py",
        "ui.py",
        "wizards.py",
        "wizard_handlers.py",
        "wizard_operators.py",
        "ops.py",
    ]
    
    for file in required_child_files:
        file_path = os.path.join(child_addon_dir, file)
        if os.path.exists(file_path):
            print(f"✓ Child file exists: {file}")
        else:
            print(f"✗ Missing child file: {file}")
            return False
    
    # Check that parent functional files are empty
    empty_parent_files = [
        "panels.py",
        "ui.py",
        "ops.py",
        "wizards.py",
        "wizard_handlers.py",
        "wizard_operators.py",
    ]
    
    for file in empty_parent_files:
        file_path = os.path.join(addon_dir, file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if "intentionally empty" in content or "Empty register" in content:
                    print(f"✓ Parent file is properly empty: {file}")
                else:
                    print(f"✗ Parent file not empty: {file}")
                    return False
        else:
            print(f"✓ Parent file missing (expected for modular): {file}")
    
    print("✅ File structure tests passed")
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Modular Asset Library Architecture")
    print("=" * 60)
    
    tests = [
        ("Utility Functions", test_utility_functions),
        ("Child Addon Management", test_child_addon_management),
        ("Library Tracking", test_library_tracking),
        ("File Structure", test_file_structure),
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"Running: {test_name}")
        print(f"{'='*40}")
        try:
            if not test_func():
                all_passed = False
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nModular architecture is correctly implemented.")
        print("The addon should work as follows:")
        print("1. Parent addon manages libraries and child addon")
        print("2. Child addon contains all functionality")
        print("3. When parent is enabled, child is automatically installed")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease check the implementation and fix the issues.")
    
    print(f"{'='*60}")
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)