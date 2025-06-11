#!/bin/bash

# Start script for Todo Flask Backend
# This script activates the virtual environment and starts the Flask development server

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Todo Flask Backend...${NC}"
echo "Working directory: $SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Error: Virtual environment not found at venv/${NC}"
    echo "Please run the setup script first to create the virtual environment."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if Flask dependencies are installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Flask not installed in virtual environment${NC}"
    echo "Please run 'pip install -r requirements.txt' first."
    exit 1
fi

# Set environment variables for development
export FLASK_ENV=development
export FLASK_DEBUG=true
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5000

echo -e "${GREEN}Starting Flask development server...${NC}"
echo "Server will be available at: http://127.0.0.1:5000"
echo "API endpoints will be available at: http://127.0.0.1:5000/api"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start the Flask application
python run.py