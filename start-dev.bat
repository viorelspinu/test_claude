@echo off
REM Development Environment Startup Script for Windows
REM This script starts both the backend Flask server and frontend React development server

setlocal enabledelayedexpansion

REM Configuration
set PROJECT_ROOT=%~dp0
set BACKEND_DIR=%PROJECT_ROOT%backend
set FRONTEND_DIR=%PROJECT_ROOT%frontend
set BACKEND_PORT=5001
set FRONTEND_PORT=3000

REM Colors (Windows 10+)
set RED=[91m
set GREEN=[92m
set YELLOW=[93m
set BLUE=[94m
set CYAN=[96m
set NC=[0m

echo %BLUE%Starting Development Environment%NC%
echo ==================================

REM Check requirements
echo.
echo %BLUE%Checking requirements...%NC%

REM Check Node.js
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Node.js is not installed. Please install Node.js 16 or higher.%NC%
    pause
    exit /b 1
)

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Python is not installed. Please install Python 3.8 or higher.%NC%
    pause
    exit /b 1
)

REM Check npm
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %RED%npm is not installed. Please install npm.%NC%
    pause
    exit /b 1
)

echo %GREEN%All requirements met%NC%

REM Setup environment
echo.
echo %BLUE%Setting up environment...%NC%

REM Create log directories
if not exist "%BACKEND_DIR%\logs" mkdir "%BACKEND_DIR%\logs"
if not exist "%FRONTEND_DIR%\logs" mkdir "%FRONTEND_DIR%\logs"

REM Check if virtual environment exists
if not exist "%BACKEND_DIR%\venv" (
    echo %YELLOW%Virtual environment not found. Creating...%NC%
    cd /d "%BACKEND_DIR%"
    python -m venv venv
)

REM Check if backend dependencies are installed
cd /d "%BACKEND_DIR%"
call venv\Scripts\activate.bat
pip show flask >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %YELLOW%Backend dependencies not installed. Installing...%NC%
    pip install -r requirements.txt
)

REM Check if frontend dependencies are installed
if not exist "%FRONTEND_DIR%\node_modules" (
    echo %YELLOW%Frontend dependencies not installed. Installing...%NC%
    cd /d "%FRONTEND_DIR%"
    call npm install
)

REM Initialize database if it doesn't exist
if not exist "%BACKEND_DIR%\instance\todo_dev.db" (
    echo %YELLOW%Database not found. Initializing...%NC%
    cd /d "%BACKEND_DIR%"
    python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
)

echo %GREEN%Environment setup complete%NC%

REM Kill existing processes on ports
echo.
echo %BLUE%Checking for existing processes...%NC%

REM Kill process on backend port
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%BACKEND_PORT%') do (
    echo %YELLOW%Killing process on port %BACKEND_PORT%...%NC%
    taskkill /F /PID %%a >nul 2>nul
)

REM Kill process on frontend port
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%FRONTEND_PORT%') do (
    echo %YELLOW%Killing process on port %FRONTEND_PORT%...%NC%
    taskkill /F /PID %%a >nul 2>nul
)

REM Start backend
echo.
echo %CYAN%Starting Flask backend...%NC%

cd /d "%BACKEND_DIR%"
set FLASK_APP=run.py
set FLASK_ENV=development
set FLASK_DEBUG=1

REM Start backend in new window
start "Flask Backend" /min cmd /c "venv\Scripts\activate.bat && python run.py > logs\backend.log 2>&1"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

REM Start frontend
echo.
echo %CYAN%Starting React frontend...%NC%

cd /d "%FRONTEND_DIR%"
set PORT=%FRONTEND_PORT%
set BROWSER=none

REM Start frontend in new window
start "React Frontend" /min cmd /c "npm start > logs\frontend.log 2>&1"

REM Wait for frontend to start
echo Waiting for frontend to start...
timeout /t 10 /nobreak >nul

REM Show status
echo.
echo %BLUE%Development Environment Status%NC%
echo ===============================
echo.
echo %GREEN%Backend:  http://localhost:%BACKEND_PORT%%NC%
echo %GREEN%API:      http://localhost:%BACKEND_PORT%/api%NC%
echo %GREEN%Health:   http://localhost:%BACKEND_PORT%/api/health%NC%
echo.
echo %GREEN%Frontend: http://localhost:%FRONTEND_PORT%%NC%
echo.
echo %BLUE%Logs:%NC%
echo   Backend:  %BACKEND_DIR%\logs\backend.log
echo   Frontend: %FRONTEND_DIR%\logs\frontend.log
echo.
echo %BLUE%Commands:%NC%
echo   View backend logs:  type "%BACKEND_DIR%\logs\backend.log"
echo   View frontend logs: type "%FRONTEND_DIR%\logs\frontend.log"
echo   Stop all:          Close this window and all command windows
echo.
echo %GREEN%Development environment is ready!%NC%
echo    Frontend: http://localhost:%FRONTEND_PORT%
echo    Backend:  http://localhost:%BACKEND_PORT%/api
echo.
echo Press any key to open the application in your browser...
pause >nul

REM Open browser
start http://localhost:%FRONTEND_PORT%

echo.
echo %YELLOW%Keep this window open to keep the servers running.%NC%
echo %YELLOW%Press Ctrl+C or close this window to stop all services.%NC%
pause >nul