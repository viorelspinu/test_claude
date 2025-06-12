import sys
import os
import subprocess

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), '../../../backend')
sys.path.insert(0, os.path.abspath(backend_path))

def test_pytest_configuration_exists():
    """Test pytest.ini configuration file exists"""
    config_file = os.path.join(backend_path, 'pytest.ini')
    assert os.path.exists(config_file), "pytest.ini should exist"

def test_test_app_exists():
    """Test test_app.py file exists"""
    test_file = os.path.join(backend_path, 'test_app.py')
    assert os.path.exists(test_file), "test_app.py should exist"

def test_pytest_configuration_content():
    """Test pytest.ini contains proper configuration"""
    config_file = os.path.join(backend_path, 'pytest.ini')
    with open(config_file, 'r') as f:
        content = f.read()
    
    assert 'testpaths' in content
    assert 'python_files = test_*.py' in content
    assert '--cov=' in content
    assert '--verbose' in content

def test_test_app_fixtures():
    """Test test_app.py contains proper fixtures"""
    test_file = os.path.join(backend_path, 'test_app.py')
    with open(test_file, 'r') as f:
        content = f.read()
    
    assert '@pytest.fixture' in content
    assert 'def client():' in content
    assert 'autouse=True' in content
    assert 'setup_teardown' in content

def test_test_app_structure():
    """Test test_app.py has proper test structure"""
    test_file = os.path.join(backend_path, 'test_app.py')
    with open(test_file, 'r') as f:
        content = f.read()
    
    assert 'class TestHealthEndpoint:' in content
    assert 'class TestTodosAPI:' in content
    assert 'class TestErrorHandling:' in content
    assert 'def test_' in content

def test_pytest_runs_successfully():
    """Test pytest command runs without errors"""
    try:
        result = subprocess.run(
            ['python', '-m', 'pytest', 'test_app.py', '-v'],
            cwd=backend_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"pytest failed: {result.stderr}"
        assert 'passed' in result.stdout
    except subprocess.TimeoutExpired:
        assert False, "pytest command timed out"
    except Exception as e:
        assert False, f"pytest command failed: {e}"

def test_sample_tests_exist():
    """Test sample tests for API endpoints exist"""
    test_file = os.path.join(backend_path, 'test_app.py')
    with open(test_file, 'r') as f:
        content = f.read()
    
    assert 'test_health_check' in content
    assert 'test_get_empty_todos' in content
    assert 'test_create_todo' in content
    assert 'test_404_error' in content
    assert 'test_405_error' in content

if __name__ == '__main__':
    test_pytest_configuration_exists()
    test_test_app_exists()
    test_pytest_configuration_content()
    test_test_app_fixtures()
    test_test_app_structure()
    test_pytest_runs_successfully()
    test_sample_tests_exist()
    print("All backend testing setup tests passed!")