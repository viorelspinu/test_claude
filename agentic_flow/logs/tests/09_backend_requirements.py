import sys
import os
import subprocess

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

def test_requirements_file_exists():
    """Test requirements.txt file exists"""
    req_file = os.path.join(backend_path, 'requirements.txt')
    assert os.path.exists(req_file), "requirements.txt should exist"

def test_requirements_content():
    """Test requirements.txt contains expected packages"""
    req_file = os.path.join(backend_path, 'requirements.txt')
    with open(req_file, 'r') as f:
        content = f.read()
    
    assert 'Flask==' in content
    assert 'Flask-CORS==' in content
    assert 'pytest==' in content
    assert 'pytest-cov==' in content

def test_flask_import():
    """Test Flask can be imported"""
    try:
        from flask import Flask
        assert True
    except ImportError:
        assert False, "Flask import failed"

def test_flask_cors_import():
    """Test Flask-CORS can be imported"""
    try:
        from flask_cors import CORS
        assert True
    except ImportError:
        assert False, "Flask-CORS import failed"

def test_pytest_import():
    """Test pytest can be imported"""
    try:
        import pytest
        assert True
    except ImportError:
        assert False, "pytest import failed"

def test_requirements_parseable():
    """Test all requirements are properly formatted"""
    import pkg_resources
    
    req_file = os.path.join(backend_path, 'requirements.txt')
    with open(req_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip()]
    
    for req in requirements:
        try:
            pkg_resources.Requirement.parse(req)
        except Exception as e:
            assert False, f"Requirement '{req}' is not parseable: {e}"

if __name__ == '__main__':
    test_requirements_file_exists()
    test_requirements_content()
    test_flask_import()
    test_flask_cors_import()
    test_pytest_import()
    test_requirements_parseable()
    print("All backend requirements tests passed!")