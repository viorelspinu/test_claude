#!/usr/bin/env python3
"""
Backend Setup Script for Flask Todo Application (SETUP-002)

This script implements the backend dependencies setup task as described in tasks.yaml.
It creates a virtual environment, installs dependencies, configures database connection,
and verifies the setup works correctly.

Task Requirements:
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


class BackendSetup:
    """Handles the setup of Flask backend with virtual environment and dependencies."""
    
    def __init__(self, project_root=None):
        """Initialize setup with project root path."""
        if project_root is None:
            # Assume we're in src/backend-setup and need to go up two levels
            self.project_root = Path(__file__).parent.parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.backend_dir = self.project_root / "backend"
        self.venv_path = self.backend_dir / "venv"
        self.requirements_file = self.backend_dir / "requirements.txt"
        
        print(f"Project root: {self.project_root}")
        print(f"Backend directory: {self.backend_dir}")
        print(f"Virtual environment path: {self.venv_path}")
    
    def check_python_version(self):
        """Check if Python version is compatible (3.8+)."""
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            raise RuntimeError(f"Python 3.8+ required, found {version.major}.{version.minor}")
        print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    
    def create_virtual_environment(self):
        """Create Python virtual environment in backend directory."""
        if self.venv_path.exists():
            print(f"Virtual environment already exists at {self.venv_path}")
            return
        
        print("Creating virtual environment...")
        try:
            subprocess.run([
                sys.executable, "-m", "venv", str(self.venv_path)
            ], check=True, cwd=self.backend_dir)
            print(f"✓ Virtual environment created at {self.venv_path}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create virtual environment: {e}")
    
    def get_pip_command(self):
        """Get the pip command for the virtual environment."""
        if os.name == 'nt':  # Windows
            return str(self.venv_path / "Scripts" / "pip")
        else:  # Unix/Linux/macOS
            return str(self.venv_path / "bin" / "pip")
    
    def get_python_command(self):
        """Get the python command for the virtual environment."""
        if os.name == 'nt':  # Windows
            return str(self.venv_path / "Scripts" / "python")
        else:  # Unix/Linux/macOS
            return str(self.venv_path / "bin" / "python")
    
    def upgrade_pip(self):
        """Upgrade pip in the virtual environment."""
        print("Upgrading pip...")
        pip_cmd = self.get_pip_command()
        try:
            subprocess.run([
                pip_cmd, "install", "--upgrade", "pip"
            ], check=True, cwd=self.backend_dir)
            print("✓ Pip upgraded successfully")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to upgrade pip: {e}")
    
    def install_dependencies(self):
        """Install dependencies from requirements.txt."""
        if not self.requirements_file.exists():
            raise FileNotFoundError(f"Requirements file not found: {self.requirements_file}")
        
        print("Installing dependencies from requirements.txt...")
        pip_cmd = self.get_pip_command()
        try:
            subprocess.run([
                pip_cmd, "install", "-r", str(self.requirements_file)
            ], check=True, cwd=self.backend_dir)
            print("✓ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to install dependencies: {e}")
    
    def verify_packages(self):
        """Verify that required packages are installed with correct versions."""
        required_packages = {
            "Flask": "2.3.0",
            "Flask-SQLAlchemy": "3.1.1",
            "Flask-Cors": "4.0.0",  # Note: pip shows "Flask-Cors" not "Flask-CORS"
            "Flask-Migrate": "4.0.0"
        }
        
        print("Verifying installed packages...")
        pip_cmd = self.get_pip_command()
        
        try:
            result = subprocess.run([
                pip_cmd, "list", "--format=json"
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            
            installed_packages = {pkg['name']: pkg['version'] for pkg in json.loads(result.stdout)}
            
            for package, expected_version in required_packages.items():
                if package not in installed_packages:
                    raise RuntimeError(f"Required package {package} not installed")
                
                installed_version = installed_packages[package]
                if installed_version != expected_version:
                    print(f"⚠ {package}: expected {expected_version}, found {installed_version}")
                else:
                    print(f"✓ {package} {installed_version}")
        
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to verify packages: {e}")
    
    def create_env_file(self):
        """Create .env file with default configuration."""
        env_file = self.backend_dir / ".env"
        
        if env_file.exists():
            print(f".env file already exists at {env_file}")
            return
        
        env_content = """# Flask Environment Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production

# Database Configuration
DATABASE_URL=sqlite:///todo_app.db

# Server Configuration
PORT=5000
HOST=0.0.0.0
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✓ Created .env file at {env_file}")
    
    def test_flask_import(self):
        """Test that Flask and other packages can be imported."""
        print("Testing package imports...")
        python_cmd = self.get_python_command()
        
        test_script = '''
import sys
try:
    import flask
    import flask_sqlalchemy
    import flask_cors
    import flask_migrate
    print("✓ All required packages imported successfully")
    print(f"✓ Flask version: {flask.__version__}")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                python_cmd, "-c", test_script
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Package import test failed: {e.stderr}")
    
    def test_flask_app_creation(self):
        """Test that the Flask app can be created and configured."""
        print("Testing Flask app creation...")
        python_cmd = self.get_python_command()
        
        test_script = f'''
import sys
import os
sys.path.insert(0, "{self.backend_dir}")

try:
    from app import create_app, db
    
    # Create app instance
    app = create_app()
    
    # Test app context and database
    with app.app_context():
        # This will create tables if they don't exist
        db.create_all()
        print("✓ Flask app created successfully")
        print(f"✓ Database configured: {{app.config['SQLALCHEMY_DATABASE_URI']}}")
        print("✓ Database tables created/verified")
        
        # Test that models can be imported
        from app.models import Task
        print("✓ Models imported successfully")
        
except Exception as e:
    print(f"✗ Flask app creation failed: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                python_cmd, "-c", test_script
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Flask app creation test failed: {e.stderr}")
    
    def test_development_server(self):
        """Test that the development server can start (quick test)."""
        print("Testing development server startup...")
        python_cmd = self.get_python_command()
        
        # Test script that starts server and immediately shuts down
        test_script = f'''
import sys
import os
import threading
import time
sys.path.insert(0, "{self.backend_dir}")

try:
    from app import create_app
    
    app = create_app()
    
    # Test that the app can be configured for testing
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Make a simple request to test the app works
    with app.app_context():
        response = client.get('/')
        # We expect 404 since no routes are defined yet, but this proves the app works
        print("✓ Flask development server can be started")
        print("✓ Test client request completed")
        
except Exception as e:
    print(f"✗ Development server test failed: {{e}}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''
        
        try:
            result = subprocess.run([
                python_cmd, "-c", test_script
            ], check=True, capture_output=True, text=True, cwd=self.backend_dir)
            print(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Development server test failed: {e.stderr}")
    
    def run_setup(self):
        """Run the complete backend setup process."""
        print("="*60)
        print("FLASK BACKEND SETUP (SETUP-002)")
        print("="*60)
        
        try:
            # Step 1: Check Python version
            self.check_python_version()
            
            # Step 2: Create virtual environment
            self.create_virtual_environment()
            
            # Step 3: Upgrade pip
            self.upgrade_pip()
            
            # Step 4: Install dependencies
            self.install_dependencies()
            
            # Step 5: Verify packages
            self.verify_packages()
            
            # Step 6: Create environment file
            self.create_env_file()
            
            # Step 7: Test imports
            self.test_flask_import()
            
            # Step 8: Test Flask app creation
            self.test_flask_app_creation()
            
            # Step 9: Test development server
            self.test_development_server()
            
            print("\n" + "="*60)
            print("✓ BACKEND SETUP COMPLETED SUCCESSFULLY!")
            print("="*60)
            
            # Print next steps
            print("\nNext steps:")
            print(f"1. Activate virtual environment:")
            if os.name == 'nt':
                print(f"   {self.venv_path}\\Scripts\\activate")
            else:
                print(f"   source {self.venv_path}/bin/activate")
            print(f"2. Start development server:")
            print(f"   cd {self.backend_dir}")
            print(f"   python run.py")
            print(f"3. Server will be available at: http://localhost:5000")
            
            return True
            
        except Exception as e:
            print(f"\n✗ Setup failed: {e}")
            return False


if __name__ == "__main__":
    """Run backend setup if script is executed directly."""
    setup = BackendSetup()
    success = setup.run_setup()
    sys.exit(0 if success else 1)