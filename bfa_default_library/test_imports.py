# Test script to verify module syntax and structure
# This test runs outside Blender, so it only checks for syntax errors
# and basic module structure without importing Blender-specific modules

import sys
import os
import ast

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def check_syntax(file_path):
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e}"

def test_module_syntax():
    """Test syntax of all Python modules"""
    print("Testing module syntax...")
    
    modules_to_test = [
        ("operators/geometry_nodes.py", "Geometry Nodes operators"),
        ("operators/compositor.py", "Compositor operators"), 
        ("operators/shader.py", "Shader operators"),
        ("operators/__init__.py", "Operators module"),
        ("wizards.py", "Wizards module"),
        ("ops.py", "Main operations"),
        ("ui.py", "UI module"),
        ("handlers_collections.py", "Handlers collections"),
        ("__init__.py", "Main addon")
    ]
    
    all_good = True
    for file_path, description in modules_to_test:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            success, error = check_syntax(full_path)
            if success:
                print(f"✓ {description} syntax is valid")
            else:
                print(f"✗ {description} syntax error: {error}")
                all_good = False
        else:
            print(f"✗ {description} file not found: {file_path}")
            all_good = False
    
    return all_good

def test_module_structure():
    """Test basic module structure without Blender imports"""
    print("\nTesting module structure...")
    
    # Test operators module structure
    try:
        # Read operators __init__ to check class references
        with open(os.path.join(os.path.dirname(__file__), 'operators', '__init__.py'), 'r') as f:
            content = f.read()
        
        # Check if operator_classes tuple is defined
        if 'operator_classes' in content:
            print("✓ Operators module has operator_classes tuple")
        else:
            print("✗ Operators module missing operator_classes tuple")
        
        # Check if register/unregister functions are defined
        if 'def register():' in content and 'def unregister():' in content:
            print("✓ Operators module has register/unregister functions")
        else:
            print("✗ Operators module missing register/unregister functions")
            
    except Exception as e:
        print(f"✗ Error testing operators structure: {e}")

if __name__ == "__main__":
    print("Running syntax and structure tests (outside Blender)...")
    syntax_ok = test_module_syntax()
    test_module_structure()
    
    if syntax_ok:
        print("\n✓ All modules have valid syntax!")
        print("Note: Blender-specific imports will fail outside Blender - this is normal")
    else:
        print("\n✗ Some modules have syntax errors")
