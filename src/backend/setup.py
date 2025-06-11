#!/usr/bin/env python3
"""
Setup script for the Todo Flask application.

This script helps set up the development environment by creating a virtual environment
and installing dependencies. It can be run to quickly bootstrap the application.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path


def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True,
            cwd=cwd
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e.stderr}")
        return None


def create_virtual_environment():
    """Create a Python virtual environment."""
    venv_path = Path.cwd() / "venv"
    
    if venv_path.exists():
        print("Virtual environment already exists at 'venv/'")
        return str(venv_path)
    
    print("Creating virtual environment...")
    venv.create(venv_path, with_pip=True)
    print(f"Virtual environment created at {venv_path}")
    
    return str(venv_path)


def install_dependencies(venv_path):
    """Install Python dependencies in the virtual environment."""
    print("Installing dependencies...")
    
    # Determine the correct python executable path
    if sys.platform == "win32":
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
        pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        python_exe = os.path.join(venv_path, "bin", "python")
        pip_exe = os.path.join(venv_path, "bin", "pip")
    
    # Upgrade pip first
    upgrade_result = run_command(f'"{pip_exe}" install --upgrade pip')
    if upgrade_result is None:
        print("Warning: Failed to upgrade pip")
    
    # Install requirements
    install_result = run_command(f'"{pip_exe}" install -r requirements.txt')
    if install_result is None:
        print("Error: Failed to install dependencies")
        return False
    
    print("Dependencies installed successfully")
    return True


def create_env_file():
    """Create a .env file with default environment variables."""
    env_file = Path.cwd() / ".env"
    
    if env_file.exists():
        print(".env file already exists")
        return
    
    env_content = """# Flask Environment Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Database Configuration
DEV_DATABASE_URL=sqlite:///development.db
TEST_DATABASE_URL=sqlite:///:memory:

# Security (change in production)
SECRET_KEY=dev-secret-key-change-in-production

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
"""
    
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(".env file created with default configuration")


def display_instructions():
    """Display instructions for running the application."""
    print("\n" + "="*60)
    print("Setup completed successfully!")
    print("="*60)
    print("\nTo run the application:")
    print("\n1. Activate the virtual environment:")
    
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Start the Flask application:")
    print("   python run.py")
    
    print("\n3. The application will be available at:")
    print("   http://127.0.0.1:5000")
    
    print("\n4. Test the health endpoint:")
    print("   curl http://127.0.0.1:5000/api/health")
    
    print("\nEnvironment variables can be configured in the .env file")
    print("="*60)


def main():
    """Main setup function."""
    print("Todo Flask Application Setup")
    print("-" * 40)
    
    # Ensure we're in the correct directory
    if not Path("requirements.txt").exists():
        print("Error: requirements.txt not found. Make sure you're in the backend directory.")
        sys.exit(1)
    
    # Create virtual environment
    venv_path = create_virtual_environment()
    
    # Install dependencies
    if not install_dependencies(venv_path):
        print("Setup failed due to dependency installation error")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Display instructions
    display_instructions()


if __name__ == "__main__":
    main()