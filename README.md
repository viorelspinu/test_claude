# Todo Application - Quick Start Guide

A full-stack Todo application with Flask backend and React frontend. This guide will help you get the application running locally in minutes.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
  - Verify installation: `python --version` or `python3 --version`
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
  - Verify installation: `node --version`
- **npm 8+** (comes with Node.js)
  - Verify installation: `npm --version`

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **Memory**: 4GB RAM minimum
- **Storage**: 500MB free space for dependencies

## Quick Start (Recommended)

### 1. Clone and Navigate
```bash
cd /path/to/your/projects
# If you haven't cloned yet:
# git clone <repository-url>
cd test_claude
```

### 2. Backend Setup (Terminal 1)
```bash
# Navigate to backend directory
cd src/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python run.py
```

**✅ Backend Verification**: You should see:
```
Starting Todo Flask application...
Environment: development
Host: 127.0.0.1
Port: 5000
Debug: True
Database tables created/verified successfully
* Running on http://127.0.0.1:5000
```

### 3. Frontend Setup (Terminal 2 - New Terminal)
```bash
# Navigate to frontend directory (from project root)
cd src/frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

**✅ Frontend Verification**: You should see:
```
  Local:   http://localhost:3000/
  Network: use --host to expose
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api

The frontend will automatically proxy API requests to the backend.

## Detailed Setup Instructions

### Backend Configuration

#### Environment Variables (Optional)
Create a `.env` file in `src/backend/` for custom configuration:
```bash
# src/backend/.env
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here
```

#### Database Location
- **Development**: SQLite database is created at `src/development.db`
- **Automatic Setup**: Database tables are created automatically on first run
- **No Manual Setup Required**: The application handles database initialization

#### Available Backend Endpoints
- `GET /api/health` - Health check
- `GET /api/` - API information
- `GET /api/todos` - List todos
- `POST /api/todos` - Create todo
- `PUT /api/todos/:id` - Update todo
- `DELETE /api/todos/:id` - Delete todo
- `GET /api/todos/stats` - Get statistics

### Frontend Configuration

#### Development Server
- **Port**: 3000 (configured in `vite.config.js`)
- **Auto-reload**: Enabled for code changes
- **API Proxy**: Automatically proxies `/api/*` requests to backend

#### Build for Production
```bash
cd src/frontend
npm run build
```
Built files will be in `src/frontend/dist/`

## Application Features

### Todo Management
- ✅ Create, read, update, delete todos
- ✅ Mark todos as complete/incomplete
- ✅ Bulk operations (complete all, delete completed)
- ✅ Real-time statistics
- ✅ Progress indicators
- ✅ Responsive design

### Technical Features
- ✅ RESTful API with Flask
- ✅ React with modern hooks
- ✅ SQLite database
- ✅ CORS configured
- ✅ Input validation
- ✅ Error handling
- ✅ Modular component architecture

## Development Workflow

### Making Changes

#### Backend Changes
1. Edit files in `src/backend/`
2. Server auto-reloads in debug mode
3. Check terminal for errors
4. Test endpoints at http://localhost:5000/api

#### Frontend Changes
1. Edit files in `src/frontend/src/`
2. Browser auto-reloads via Vite
3. Check browser console for errors
4. Changes reflect immediately

### Testing

#### Backend Tests
```bash
cd src/backend
source venv/bin/activate  # If not already activated
pytest
```

#### Code Quality (Backend)
```bash
cd src/backend
flake8 .          # Check code style
black .           # Format code
```

#### Frontend Linting
```bash
cd src/frontend
npm run lint      # Check code style
```

## Troubleshooting

### Common Issues

#### Backend Won't Start
**Problem**: `ModuleNotFoundError` or import errors
**Solution**: 
```bash
cd src/backend
source venv/bin/activate
pip install -r requirements.txt
```

**Problem**: Port 5000 already in use
**Solution**: 
```bash
export FLASK_PORT=5001  # Use different port
python run.py
```

#### Frontend Won't Start
**Problem**: `npm install` fails
**Solution**:
```bash
cd src/frontend
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Port 3000 already in use
**Solution**: Vite will prompt to use a different port (usually 3001)

#### API Connection Issues
**Problem**: Frontend can't reach backend
**Solutions**:
1. Ensure backend is running on port 5000
2. Check browser network tab for failed requests
3. Verify CORS settings in `src/backend/config.py`

#### Database Issues
**Problem**: Database errors
**Solution**: Delete the database file and restart:
```bash
rm src/development.db
cd src/backend
python run.py  # Database will be recreated
```

### Getting Help

#### Check Application Status
```bash
# Backend health check
curl http://localhost:5000/api/health

# Frontend accessibility
curl http://localhost:3000
```

#### View Logs
- **Backend**: Logs appear in the terminal where you ran `python run.py`
- **Frontend**: Check browser developer tools console

#### Reset Everything
```bash
# Stop all servers (Ctrl+C in terminals)

# Reset backend
cd src/backend
rm -rf venv/
rm -f ../development.db

# Reset frontend
cd ../frontend
rm -rf node_modules/
rm -f package-lock.json

# Start fresh with setup instructions above
```

## Next Steps

Once you have the application running:

1. **Explore the Interface**: Create, edit, and delete todos
2. **Try Bulk Operations**: Select multiple todos and use bulk actions
3. **Check Statistics**: View the progress indicators and stats
4. **Test API Directly**: Use curl or Postman to test backend endpoints
5. **Modify Code**: Make changes and see them reflected immediately

## Project Structure Overview

```
test_claude/
├── src/
│   ├── backend/           # Flask API server
│   │   ├── app/          # Application modules
│   │   ├── requirements.txt
│   │   └── run.py        # Server entry point
│   └── frontend/         # React application
│       ├── src/          # React components
│       ├── package.json
│       └── vite.config.js
├── docs/                 # Documentation
└── README.md            # This file
```

## Support

If you encounter issues not covered in this guide:
1. Check the troubleshooting section above
2. Review backend logs in terminal
3. Check browser developer tools
4. Ensure all prerequisites are correctly installed

Happy coding! 🚀