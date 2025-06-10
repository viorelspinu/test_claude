# Backend Setup (SETUP-002)

This directory contains scripts for setting up the Flask backend with virtual environment, dependencies, and database configuration as specified in task SETUP-002.

## Files

- `setup_backend.py` - Main setup script that creates virtual environment and installs dependencies
- `verify_setup.py` - Verification script to check that setup completed successfully
- `README.md` - This documentation file

## Task Requirements (SETUP-002)

**Acceptance Criteria:**
- Flask application can start successfully
- All required dependencies installed
- Virtual environment configured
- Database connection working

**Dependencies:**
- Flask==2.3.0
- Flask-SQLAlchemy==3.0.0
- Flask-CORS==4.0.0
- Flask-Migrate==4.0.0

## Usage

### Running the Setup

```bash
# From the project root directory
cd /Users/viorel/workspace/test_claude
python src/backend-setup/setup_backend.py
```

### Verifying the Setup

```bash
# From the project root directory
python src/backend-setup/verify_setup.py
```

### Manual Steps After Setup

1. Activate the virtual environment:
   ```bash
   cd backend
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

2. Start the development server:
   ```bash
   python run.py
   ```

3. The server will be available at: http://localhost:5000

## What the Setup Does

1. **Python Version Check** - Ensures Python 3.8+ is available
2. **Virtual Environment** - Creates `backend/venv/` directory
3. **Package Installation** - Installs all requirements from `requirements.txt`
4. **Package Verification** - Confirms correct versions are installed
5. **Environment Configuration** - Creates `.env` file with default settings
6. **Import Testing** - Verifies Flask packages can be imported
7. **App Creation Testing** - Tests that Flask app can be created
8. **Database Testing** - Verifies database connection and table creation
9. **Server Testing** - Confirms development server can start

## Project Structure

After setup completion:

```
backend/
├── venv/                 # Virtual environment (created by setup)
├── app/
│   ├── __init__.py      # Flask app factory
│   └── models.py        # Database models
├── run.py               # Development server entry point
├── requirements.txt     # Python dependencies
└── .env                 # Environment configuration (created by setup)
```

## Environment Variables

The setup creates a `.env` file with these default values:

- `FLASK_ENV=development`
- `FLASK_DEBUG=True`
- `SECRET_KEY=dev-secret-key-change-in-production`
- `DATABASE_URL=sqlite:///todo_app.db`
- `PORT=5000`
- `HOST=0.0.0.0`

## Troubleshooting

If setup fails:

1. Check Python version: `python3 --version`
2. Ensure you have permissions to create directories
3. Check internet connection for package downloads
4. Review error messages in the setup output

If verification fails:
1. Re-run the setup script
2. Check that virtual environment was created
3. Manually activate venv and test imports
4. Check for error messages in verification output