#!/bin/bash

# Development Environment Startup Script
# This script starts both the backend Flask server and frontend React development server

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"
BACKEND_PORT=5001
FRONTEND_PORT=3000
BACKEND_LOG="$BACKEND_DIR/logs/backend.log"
FRONTEND_LOG="$FRONTEND_DIR/logs/frontend.log"

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to kill process on port
kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        kill -9 $pids 2>/dev/null || true
        sleep 1
    fi
}

# Function to check requirements
check_requirements() {
    print_status $BLUE "🔍 Checking requirements..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_status $RED "❌ Node.js is not installed. Please install Node.js 16 or higher."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        print_status $RED "❌ Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_status $RED "❌ npm is not installed. Please install npm."
        exit 1
    fi
    
    print_status $GREEN "✅ All requirements met"
}

# Function to setup environment
setup_environment() {
    print_status $BLUE "🔧 Setting up environment..."
    
    # Create log directories
    mkdir -p "$BACKEND_DIR/logs"
    mkdir -p "$FRONTEND_DIR/logs"
    
    # Check if virtual environment exists
    if [ ! -d "$BACKEND_DIR/venv" ]; then
        print_status $YELLOW "⚠️  Virtual environment not found. Creating..."
        cd "$BACKEND_DIR"
        python3 -m venv venv || python -m venv venv
    fi
    
    # Activate virtual environment
    source "$BACKEND_DIR/venv/bin/activate"
    
    # Check if backend dependencies are installed
    if ! pip show flask &> /dev/null; then
        print_status $YELLOW "⚠️  Backend dependencies not installed. Installing..."
        cd "$BACKEND_DIR"
        pip install -r requirements.txt
    fi
    
    # Check if frontend dependencies are installed
    if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
        print_status $YELLOW "⚠️  Frontend dependencies not installed. Installing..."
        cd "$FRONTEND_DIR"
        npm install
    fi
    
    # Initialize database if it doesn't exist
    if [ ! -f "$BACKEND_DIR/instance/todo_dev.db" ]; then
        print_status $YELLOW "⚠️  Database not found. Initializing..."
        cd "$BACKEND_DIR"
        python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
    fi
    
    print_status $GREEN "✅ Environment setup complete"
}

# Function to start backend
start_backend() {
    print_status $CYAN "🚀 Starting Flask backend..."
    
    # Check if port is already in use
    if check_port $BACKEND_PORT; then
        print_status $YELLOW "⚠️  Port $BACKEND_PORT is already in use. Attempting to kill existing process..."
        kill_port $BACKEND_PORT
    fi
    
    # Set environment variables
    export FLASK_APP=run.py
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    
    # Start backend server
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    # Run in background and save PID
    python run.py > "$BACKEND_LOG" 2>&1 &
    BACKEND_PID=$!
    
    # Wait for backend to start
    local wait_count=0
    while ! check_port $BACKEND_PORT && [ $wait_count -lt 30 ]; do
        sleep 1
        wait_count=$((wait_count + 1))
        echo -n "."
    done
    echo ""
    
    if check_port $BACKEND_PORT; then
        print_status $GREEN "✅ Backend started on port $BACKEND_PORT (PID: $BACKEND_PID)"
    else
        print_status $RED "❌ Failed to start backend"
        exit 1
    fi
}

# Function to start frontend
start_frontend() {
    print_status $CYAN "🚀 Starting React frontend..."
    
    # Check if port is already in use
    if check_port $FRONTEND_PORT; then
        print_status $YELLOW "⚠️  Port $FRONTEND_PORT is already in use. Attempting to kill existing process..."
        kill_port $FRONTEND_PORT
    fi
    
    # Set environment variables
    export PORT=$FRONTEND_PORT
    export BROWSER=none  # Don't auto-open browser
    
    # Start frontend server
    cd "$FRONTEND_DIR"
    
    # Run in background and save PID
    npm start > "$FRONTEND_LOG" 2>&1 &
    FRONTEND_PID=$!
    
    # Wait for frontend to start
    local wait_count=0
    while ! check_port $FRONTEND_PORT && [ $wait_count -lt 60 ]; do
        sleep 1
        wait_count=$((wait_count + 1))
        echo -n "."
    done
    echo ""
    
    if check_port $FRONTEND_PORT; then
        print_status $GREEN "✅ Frontend started on port $FRONTEND_PORT (PID: $FRONTEND_PID)"
    else
        print_status $RED "❌ Failed to start frontend"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
}

# Function to show status
show_status() {
    print_status $BLUE "\n📊 Development Environment Status"
    print_status $BLUE "================================="
    
    if check_port $BACKEND_PORT; then
        print_status $GREEN "✅ Backend:  http://localhost:$BACKEND_PORT"
        print_status $GREEN "   API:      http://localhost:$BACKEND_PORT/api"
        print_status $GREEN "   Health:   http://localhost:$BACKEND_PORT/api/health"
    else
        print_status $RED "❌ Backend:  Not running"
    fi
    
    if check_port $FRONTEND_PORT; then
        print_status $GREEN "✅ Frontend: http://localhost:$FRONTEND_PORT"
    else
        print_status $RED "❌ Frontend: Not running"
    fi
    
    print_status $BLUE "\n📝 Logs:"
    print_status $BLUE "  Backend:  $BACKEND_LOG"
    print_status $BLUE "  Frontend: $FRONTEND_LOG"
    
    print_status $BLUE "\n🛠️  Commands:"
    print_status $BLUE "  View backend logs:  tail -f $BACKEND_LOG"
    print_status $BLUE "  View frontend logs: tail -f $FRONTEND_LOG"
    print_status $BLUE "  Stop all:          Press Ctrl+C"
}

# Function to handle cleanup
cleanup() {
    print_status $YELLOW "\n🛑 Shutting down development environment..."
    
    # Kill backend process
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        print_status $YELLOW "   Stopped backend (PID: $BACKEND_PID)"
    fi
    
    # Kill frontend process
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        print_status $YELLOW "   Stopped frontend (PID: $FRONTEND_PID)"
    fi
    
    # Kill any remaining processes on ports
    kill_port $BACKEND_PORT
    kill_port $FRONTEND_PORT
    
    print_status $GREEN "✅ Shutdown complete"
    exit 0
}

# Main execution
main() {
    print_status $BLUE "🚀 Starting Development Environment"
    print_status $BLUE "==================================\n"
    
    # Set trap for cleanup on exit
    trap cleanup EXIT INT TERM
    
    # Check requirements
    check_requirements
    
    # Setup environment
    setup_environment
    
    # Start services
    start_backend
    start_frontend
    
    # Show status
    show_status
    
    print_status $GREEN "\n✨ Development environment is ready!"
    print_status $GREEN "   Frontend: http://localhost:$FRONTEND_PORT"
    print_status $GREEN "   Backend:  http://localhost:$BACKEND_PORT/api"
    
    # Keep script running and show logs
    print_status $YELLOW "\n📋 Showing combined logs (Press Ctrl+C to stop)...\n"
    
    # Tail both log files
    tail -f "$BACKEND_LOG" "$FRONTEND_LOG" 2>/dev/null || {
        # If tail fails, just wait
        print_status $YELLOW "Waiting... (Press Ctrl+C to stop)"
        while true; do
            sleep 1
        done
    }
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Development Environment Startup Script"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  --help, -h        Show this help message"
        echo "  --backend-only    Start only the backend server"
        echo "  --frontend-only   Start only the frontend server"
        echo "  --check           Check if services are running"
        echo "  --stop            Stop all services"
        echo ""
        exit 0
        ;;
    --backend-only)
        check_requirements
        setup_environment
        start_backend
        show_status
        print_status $YELLOW "\nBackend running (Press Ctrl+C to stop)..."
        tail -f "$BACKEND_LOG" 2>/dev/null || wait $BACKEND_PID
        ;;
    --frontend-only)
        check_requirements
        setup_environment
        start_frontend
        show_status
        print_status $YELLOW "\nFrontend running (Press Ctrl+C to stop)..."
        tail -f "$FRONTEND_LOG" 2>/dev/null || wait $FRONTEND_PID
        ;;
    --check)
        show_status
        exit 0
        ;;
    --stop)
        print_status $YELLOW "Stopping all services..."
        kill_port $BACKEND_PORT
        kill_port $FRONTEND_PORT
        print_status $GREEN "✅ All services stopped"
        exit 0
        ;;
    *)
        main
        ;;
esac