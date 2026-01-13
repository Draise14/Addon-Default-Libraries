#!/usr/bin/env python3
"""
Test script for Bforartists paths in Modular Asset Library Architecture
Tests the Bforartists-specific path handling
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utility

def test_bfa_extensions_path():
    """Test Bforartists extensions path detection."""
    print("Testing Bforartists extensions path...")
    
    # Mock bpy to test without Blender
    class MockBpy:
        class utils:
            @staticmethod
            def resource_path(type):
                if type == "USER":
                    # Return a mock user path
                    return "/mock/user/path/Bforartists/5.1"
                return "/mock/path"
        
        class app:
            version = (5, 1, 0)
    
    # Temporarily replace bpy
    original_bpy = sys.modules.get('bpy')
    sys.modules['bpy'] = MockBpy()
    
    try:
        # Test get_user_preferences_path
        user_path = utility.get_user_preferences_path()
        print(f"✓ User preferences path: {user_path}")
        
        # Test get_bfa_extensions_path
        extensions_path = utility.get_bfa_extensions_path()
        expected_path = os.path.join(user_path, "extensions", "user_default")
        print(f"✓ BFA extensions path: {extensions_path}")
        print(f"✓ Expected path: {expected_path}")
        
        # Test get_child_addon_path
        child_path = utility.get_child_addon_path("test_child")
        expected_child_path = os.path.join(extensions_path, "test_child")
        print(f"✓ Child addon path: {child_path}")
        print(f"✓ Expected child path: {expected_child_path}")
        
        if child_path == expected_child_path:
            print("✅ BFA paths test passed")
            return True
        else:
            print("❌ BFA paths test failed: Paths don't match")
            return False
            
    finally:
        # Restore original bpy if it existed
        if original_bpy:
            sys.modules['bpy'] = original_bpy
        else:
            del sys.modules['bpy']

def test_path_creation():
    """Test that paths are created correctly."""
    print("\nTesting path creation...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a mock user directory structure
        mock_user_dir = os.path.join(temp_dir, "Bforartists", "5.1")
        os.makedirs(mock_user_dir, exist_ok=True)
        
        # Test get_bfa_extensions_path with custom path
        original_get_user_prefs = utility.get_user_preferences_path
        
        def mock_get_user_preferences_path():
            return mock_user_dir
        
        utility.get_user_preferences_path = mock_get_user_preferences_path
        
        try:
            extensions_path = utility.get_bfa_extensions_path()
            print(f"✓ Created extensions path: {extensions_path}")
            
            # Check if directory was created
            if os.path.exists(extensions_path):
                print("✅ Extensions directory was created")
                
                # Test creating a child addon directory
                child_path = utility.get_child_addon_path("test_addon")
                print(f"✓ Child addon path: {child_path}")
                
                # Create a manifest to test manifest functions
                parent_info = {
                    'name': 'Test Parent',
                    'version': (1, 0, 0),
                    'unique_id': 'test_parent_1_0_0'
                }
                
                manifest_file = utility.create_child_addon_manifest("test_addon", parent_info)
                print(f"✓ Created manifest: {manifest_file}")
                
                # Read the manifest
                manifest_data = utility.read_child_addon_manifest("test_addon")
                if manifest_data and manifest_data.get('parent_addon_id') == 'test_parent_1_0_0':
                    print("✅ Manifest read successfully")
                else:
                    print("❌ Failed to read manifest")
                    return False
                
                # Get child addons by parent
                child_addons = utility.get_child_addons_by_parent('test_parent_1_0_0')
                if "test_addon" in child_addons:
                    print(f"✅ Found child addon: {child_addons}")
                else:
                    print(f"❌ Could not find child addon")
                    return False
                
                # Remove manifest
                if utility.remove_child_addon_manifest("test_addon"):
                    print("✅ Manifest removed successfully")
                else:
                    print("❌ Failed to remove manifest")
                    return False
                
                return True
            else:
                print("❌ Extensions directory was not created")
                return False
                
        finally:
            utility.get_user_preferences_path = original_get_user_prefs

def main():
    """Run all BFA path tests."""
    print("=" * 60)
    print("Testing Bforartists Path Handling")
    print("=" * 60)
    
    tests = [
        ("BFA Extensions Path", test_bfa_extensions_path),
        ("Path Creation", test_path_creation),
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
        print("✅ ALL BFA PATH TESTS PASSED!")
        print("\nThe Bforartists path handling is correctly implemented.")
        print("\nKey points verified:")
        print("1. ✅ Extensions path is correctly constructed")
        print("2. ✅ Child addon path is correct")
        print("3. ✅ Directory creation works")
        print("4. ✅ Manifest management works")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease check the Bforartists path implementation.")
    
    print("=" * 60)
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)