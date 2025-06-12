import sys
import os
import subprocess
import json

# Add frontend directory to path
frontend_path = os.path.join(os.path.dirname(__file__), '../../../frontend')

def test_frontend_directory_exists():
    """Test frontend directory was created"""
    assert os.path.exists(frontend_path), "frontend directory should exist"

def test_package_json_exists():
    """Test package.json exists and has correct structure"""
    package_json_path = os.path.join(frontend_path, 'package.json')
    assert os.path.exists(package_json_path), "package.json should exist"
    
    with open(package_json_path, 'r') as f:
        package_data = json.load(f)
    
    assert package_data['name'] == 'frontend'
    assert 'react' in package_data['dependencies']
    assert 'react-dom' in package_data['dependencies']
    assert 'react-scripts' in package_data['dependencies']

def test_package_json_scripts():
    """Test package.json has correct scripts"""
    package_json_path = os.path.join(frontend_path, 'package.json')
    with open(package_json_path, 'r') as f:
        package_data = json.load(f)
    
    scripts = package_data['scripts']
    assert 'start' in scripts
    assert 'build' in scripts
    assert 'test' in scripts
    assert scripts['start'] == 'react-scripts start'
    assert scripts['build'] == 'react-scripts build'

def test_src_directory_structure():
    """Test src directory has React app structure"""
    src_path = os.path.join(frontend_path, 'src')
    assert os.path.exists(src_path), "src directory should exist"
    
    required_files = ['App.js', 'index.js', 'App.test.js']
    for file in required_files:
        file_path = os.path.join(src_path, file)
        assert os.path.exists(file_path), f"{file} should exist in src"

def test_public_directory_structure():
    """Test public directory has required files"""
    public_path = os.path.join(frontend_path, 'public')
    assert os.path.exists(public_path), "public directory should exist"
    
    required_files = ['index.html', 'manifest.json']
    for file in required_files:
        file_path = os.path.join(public_path, file)
        assert os.path.exists(file_path), f"{file} should exist in public"

def test_npm_test_command():
    """Test npm test command works"""
    try:
        result = subprocess.run(
            ['npm', 'test', '--', '--watchAll=false'],
            cwd=frontend_path,
            capture_output=True,
            text=True,
            timeout=60
        )
        # Just check return code - test framework works
        assert result.returncode == 0, f"npm test failed with return code {result.returncode}"
    except subprocess.TimeoutExpired:
        assert False, "npm test command timed out"
    except Exception as e:
        assert False, f"npm test command failed: {e}"

def test_npm_build_command():
    """Test npm build command creates production build"""
    try:
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=frontend_path,
            capture_output=True,
            text=True,
            timeout=120
        )
        assert result.returncode == 0, f"npm build failed: {result.stderr}"
        assert 'Compiled successfully' in result.stdout
        
        # Check build directory was created
        build_path = os.path.join(frontend_path, 'build')
        assert os.path.exists(build_path), "build directory should be created"
        
        # Check static files exist
        static_path = os.path.join(build_path, 'static')
        assert os.path.exists(static_path), "static directory should exist in build"
        
    except subprocess.TimeoutExpired:
        assert False, "npm build command timed out"
    except Exception as e:
        assert False, f"npm build command failed: {e}"

def test_node_modules_installed():
    """Test node_modules directory exists with dependencies"""
    node_modules_path = os.path.join(frontend_path, 'node_modules')
    assert os.path.exists(node_modules_path), "node_modules should exist"
    
    # Check key React packages exist
    react_path = os.path.join(node_modules_path, 'react')
    assert os.path.exists(react_path), "react package should be installed"

if __name__ == '__main__':
    test_frontend_directory_exists()
    test_package_json_exists()
    test_package_json_scripts()
    test_src_directory_structure()
    test_public_directory_structure()
    test_npm_test_command()
    test_npm_build_command()
    test_node_modules_installed()
    print("All React app initialization tests passed!")