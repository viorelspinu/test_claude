#!/usr/bin/env python3
"""
Backend Setup Verification Script

This script verifies that the Flask backend setup (SETUP-002) was completed successfully.
It checks all acceptance criteria from the tasks.yaml file.

Acceptance Criteria:
- Flask application can start successfully
- All required dependencies installed
- Virtual environment configured
- Database connection working
"""

import os
import sys
import subprocess
import json
from pathlib import Path


class SetupVerifier:
    """Verifies the Flask backend setup is working correctly."""
    
    def __init__(self, project_root=None):
        """Initialize verifier with project root path."""
        if project_root is None:
            self.project_root = Path(__file__).parent.parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.backend_dir = self.project_root / "backend"
        self.venv_path = self.backend_dir / "venv"
        self.requirements_file = self.backend_dir / "requirements.txt"
        
        self.results = []
    
    def log_result(self, test_name, passed, message=""):
        """Log test result."""
        status = "✓ PASS" if passed else "✗ FAIL"
        result = f"{status}: {test_name}"
        if message:
            result += f" - {message}"
        print(result)
        self.results.append((test_name, passed, message))
    
    def check_virtual_environment(self):
        """Check that virtual environment exists and is configured."""
        test_name = "Virtual Environment Configuration"
        
        if not self.venv_path.exists():
            self.log_result(test_name, False, "Virtual environment directory not found")
            return False
        
        # Check for Python executable
        if os.name == 'nt':  # Windows
            python_exe = self.venv_path / "Scripts" / "python.exe"
            pip_exe = self.venv_path / "Scripts" / "pip.exe"
        else:  # Unix/Linux/macOS
            python_exe = self.venv_path / "bin" / "python"
            pip_exe = self.venv_path / "bin" / "pip"
        
        if not python_exe.exists():
            self.log_result(test_name, False, "Python executable not found in venv")
            return False
        
        if not pip_exe.exists():
            self.log_result(test_name, False, "Pip executable not found in venv")
            return False
        
        self.log_result(test_name, True, f"Virtual environment found at {self.venv_path}")
        return True
    
    def check_dependencies_installed(self):
        """Check that all required dependencies are installed."""
        test_name = "Required Dependencies Installed"
        
        required_packages = [
            "Flask", "Flask-SQLAlchemy", "Flask-Cors", "Flask-Migrate", "python-dotenv"
        ]
        
        # Get pip command
        if os.name == 'nt':
            pip_cmd = str(self.venv_path / "Scripts" / "pip")
        else:
            pip_cmd = str(self.venv_path / "bin" / "pip")
        
        try:
            result = subprocess.run([
                pip_cmd, "list", "--format=json"
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            
            installed_packages = {pkg['name'] for pkg in json.loads(result.stdout)}
            missing_packages = [pkg for pkg in required_packages if pkg not in installed_packages]
            
            if missing_packages:
                self.log_result(test_name, False, f"Missing packages: {', '.join(missing_packages)}")
                return False
            
            self.log_result(test_name, True, f"All required packages installed: {', '.join(required_packages)}")
            return True
            
        except Exception as e:
            self.log_result(test_name, False, f"Error checking packages: {e}")
            return False
    
    def check_flask_import(self):
        """Check that Flask and related packages can be imported."""
        test_name = "Flask Package Import"
        
        if os.name == 'nt':
            python_cmd = str(self.venv_path / "Scripts" / "python")
        else:
            python_cmd = str(self.venv_path / "bin" / "python")
        
        test_script = '''
try:
    import flask
    import flask_sqlalchemy
    import flask_cors
    import flask_migrate
    import flask.cli
    print("SUCCESS")
except ImportError as e:
    print(f"IMPORT_ERROR: {e}")
'''
        
        try:
            result = subprocess.run([
                python_cmd, "-c", test_script
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            
            if "SUCCESS" in result.stdout:
                self.log_result(test_name, True, "All Flask packages import successfully")
                return True
            else:
                self.log_result(test_name, False, result.stdout.strip())
                return False
                
        except subprocess.CalledProcessError as e:
            self.log_result(test_name, False, f"Import test failed: {e.stderr}")
            return False
    
    def check_flask_app_creation(self):
        """Check that Flask app can be created successfully."""
        test_name = "Flask Application Creation"
        
        if os.name == 'nt':
            python_cmd = str(self.venv_path / "Scripts" / "python")
        else:
            python_cmd = str(self.venv_path / "bin" / "python")
        
        test_script = f'''
import sys
import os
sys.path.insert(0, "{self.backend_dir}")

try:
    from app import create_app, db
    app = create_app()
    
    if app is None:
        print("APP_CREATION_FAILED: create_app returned None")
        sys.exit(1)
    
    # Check basic configuration
    required_config = ['SQLALCHEMY_DATABASE_URI', 'SECRET_KEY']
    for key in required_config:
        if key not in app.config:
            print(f"CONFIG_MISSING: {{key}}")
            sys.exit(1)
    
    print("SUCCESS")
    
except Exception as e:
    print(f"ERROR: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                python_cmd, "-c", test_script
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            
            if "SUCCESS" in result.stdout:
                self.log_result(test_name, True, "Flask app creates successfully with proper configuration")
                return True
            else:
                self.log_result(test_name, False, result.stdout.strip())
                return False
                
        except subprocess.CalledProcessError as e:
            self.log_result(test_name, False, f"App creation test failed: {e.stderr}")
            return False
    
    def check_database_connection(self):
        """Check that database connection works and tables can be created."""
        test_name = "Database Connection and Schema"
        
        if os.name == 'nt':
            python_cmd = str(self.venv_path / "Scripts" / "python")
        else:
            python_cmd = str(self.venv_path / "bin" / "python")
        
        test_script = f'''
import sys
import os
sys.path.insert(0, "{self.backend_dir}")

try:
    from app import create_app, db
    from app.models import Task
    
    app = create_app()
    
    with app.app_context():
        # Test database connection by creating tables
        db.create_all()
        
        # Test that we can query the database
        task_count = Task.query.count()
        
        # Test that Task model has required attributes
        required_attrs = ['id', 'title', 'description', 'priority', 'completed', 'created_at']
        task_attrs = [attr for attr in dir(Task) if not attr.startswith('_')]
        
        missing_attrs = [attr for attr in required_attrs if attr not in task_attrs]
        if missing_attrs:
            print(f"MODEL_MISSING_ATTRS: {{missing_attrs}}")
            sys.exit(1)
        
        print("SUCCESS")
        
except Exception as e:
    print(f"ERROR: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                python_cmd, "-c", test_script
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            
            if "SUCCESS" in result.stdout:
                self.log_result(test_name, True, "Database connection works, tables created, models configured")
                return True
            else:
                self.log_result(test_name, False, result.stdout.strip())
                return False
                
        except subprocess.CalledProcessError as e:
            self.log_result(test_name, False, f"Database test failed: {e.stderr}")
            return False
    
    def check_development_server_startup(self):
        """Check that Flask development server can start."""
        test_name = "Development Server Startup"
        
        if os.name == 'nt':
            python_cmd = str(self.venv_path / "Scripts" / "python")
        else:
            python_cmd = str(self.venv_path / "bin" / "python")
        
        test_script = f'''
import sys
import os
sys.path.insert(0, "{self.backend_dir}")

try:
    from app import create_app
    
    app = create_app()
    app.config['TESTING'] = True
    
    # Create test client to verify app can handle requests
    client = app.test_client()
    
    # Make a test request (expecting 404 since no routes defined yet)
    response = client.get('/')
    
    # If we get here, the server can start and handle requests
    print("SUCCESS")
    
except Exception as e:
    print(f"ERROR: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                python_cmd, "-c", test_script
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            
            if "SUCCESS" in result.stdout:
                self.log_result(test_name, True, "Development server can start and handle requests")
                return True
            else:
                self.log_result(test_name, False, result.stdout.strip())
                return False
                
        except subprocess.CalledProcessError as e:
            self.log_result(test_name, False, f"Server startup test failed: {e.stderr}")
            return False
    
    def check_file_structure(self):
        """Check that all required files exist."""
        test_name = "Required Files Present"
        
        required_files = [
            self.backend_dir / "app" / "__init__.py",
            self.backend_dir / "app" / "models.py",
            self.backend_dir / "run.py",
            self.backend_dir / "requirements.txt"
        ]
        
        missing_files = [f for f in required_files if not f.exists()]
        
        if missing_files:
            self.log_result(test_name, False, f"Missing files: {[str(f) for f in missing_files]}")
            return False
        
        self.log_result(test_name, True, "All required backend files present")
        return True
    
    def run_verification(self):
        """Run all verification tests."""
        print("="*70)
        print("FLASK BACKEND SETUP VERIFICATION (SETUP-002)")
        print("="*70)
        print()
        
        # Run all tests
        tests = [
            self.check_file_structure,
            self.check_virtual_environment,
            self.check_dependencies_installed,
            self.check_flask_import,
            self.check_flask_app_creation,
            self.check_database_connection,
            self.check_development_server_startup
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test in tests:
            if test():
                passed_tests += 1
        
        print()
        print("="*70)
        print(f"VERIFICATION SUMMARY: {passed_tests}/{total_tests} tests passed")
        print("="*70)
        
        if passed_tests == total_tests:
            print("✓ ALL TESTS PASSED - Backend setup is working correctly!")
            print()
            print("Acceptance criteria verification:")
            print("✓ Flask application can start successfully")
            print("✓ All required dependencies installed")
            print("✓ Virtual environment configured")
            print("✓ Database connection working")
            return True
        else:
            print("✗ SOME TESTS FAILED - Please review the setup")
            failed_tests = [result for result in self.results if not result[1]]
            print("\nFailed tests:")
            for test_name, _, message in failed_tests:
                print(f"  - {test_name}: {message}")
            return False


if __name__ == "__main__":
    """Run verification if script is executed directly."""
    verifier = SetupVerifier()
    success = verifier.run_verification()
    sys.exit(0 if success else 1)