#!/bin/bash

# Setup script for Todo Flask Backend
# This script creates the virtual environment and installs all dependencies

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Todo Flask Backend...${NC}"
echo "Working directory: $SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${BLUE}Using Python version: $PYTHON_VERSION${NC}"

# Check if virtual environment already exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing virtual environment...${NC}"
        rm -rf venv
    else
        echo -e "${YELLOW}Using existing virtual environment${NC}"
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        echo -e "${GREEN}Dependencies updated successfully!${NC}"
        echo ""
        echo -e "${GREEN}Setup complete! You can now start the backend with:${NC}"
        echo "  ./start.sh"
        echo ""
        echo -e "${BLUE}Or manually with:${NC}"
        echo "  source venv/bin/activate"
        echo "  python run.py"
        exit 0
    fi
fi

# Create virtual environment
echo -e "${YELLOW}Creating Python virtual environment...${NC}"
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to create virtual environment${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install dependencies
echo -e "${YELLOW}Installing Python dependencies from requirements.txt...${NC}"
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi

pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install dependencies${NC}"
    exit 1
fi

# Initialize database
echo -e "${YELLOW}Initializing database...${NC}"
python -c "
from app import create_app, db
from app.models import Todo
app = create_app()
with app.app_context():
    db.create_all()
    print('Database tables created successfully')
"

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to initialize database${NC}"
    exit 1
fi

# Run tests to verify installation
echo -e "${YELLOW}Running quick verification test...${NC}"
python -c "
from app import create_app
app = create_app()
print('Flask application created successfully')
"

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Flask application test failed${NC}"
    exit 1
fi

echo -e "${GREEN}Setup completed successfully!${NC}"
echo ""
echo -e "${GREEN}You can now start the backend with:${NC}"
echo "  ./start.sh"
echo ""
echo -e "${BLUE}Or manually with:${NC}"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo -e "${BLUE}The API will be available at:${NC}"
echo "  http://127.0.0.1:5000/api"
echo ""
echo -e "${BLUE}Available endpoints:${NC}"
echo "  GET  /api/health    - Health check"
echo "  GET  /api          - API information"
echo "  GET  /api/todos    - List todos"
echo "  POST /api/todos    - Create new todo"
echo ""