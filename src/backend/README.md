# Todo Application Backend

This is the Flask backend for the Todo application, implementing a RESTful API with SQLAlchemy ORM and SQLite database.

## Project Structure

```
backend/
├── app/                    # Main application package
│   ├── __init__.py        # Flask app factory
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # API route blueprints
│   ├── schemas/           # Marshmallow schemas
│   ├── services/          # Business logic services
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── migrations/            # Database migrations
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── run.py                 # Application entry point
└── setup.py              # Development setup script
```

## Quick Start

### Option 1: Automated Setup

Run the setup script to automatically create virtual environment and install dependencies:

```bash
python setup.py
```

Then activate the virtual environment and start the server:

```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Start the server:
python run.py
```

### Option 2: Manual Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables (optional):
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
```

4. Run the application:
```bash
python run.py
```

## Configuration

The application supports multiple environments:

- **Development** (default): Debug enabled, SQLite database, verbose logging
- **Testing**: In-memory database, CSRF disabled
- **Production**: Debug disabled, security headers, production database

Environment can be set via `FLASK_ENV` variable or by passing config name to `create_app()`.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/testing/production) | development |
| `FLASK_DEBUG` | Enable debug mode | True |
| `FLASK_HOST` | Host to bind to | 127.0.0.1 |
| `FLASK_PORT` | Port to bind to | 5000 |
| `SECRET_KEY` | Flask secret key | dev-secret-key-change-in-production |
| `DEV_DATABASE_URL` | Development database URL | sqlite:///development.db |
| `TEST_DATABASE_URL` | Testing database URL | sqlite:///:memory: |
| `DATABASE_URL` | Production database URL | sqlite:///production.db |

## API Endpoints

### Health Check
- `GET /api/health` - Application and database health status

### API Information
- `GET /api` - Basic API information and available endpoints

### Future Endpoints (to be implemented)
- `GET /api/todos` - List todos with pagination and filtering
- `POST /api/todos` - Create new todo
- `GET /api/todos/:id` - Get specific todo
- `PUT /api/todos/:id` - Update existing todo
- `DELETE /api/todos/:id` - Delete todo
- `GET /api/todos/stats` - Todo statistics

## Features Implemented

✅ Flask application factory pattern  
✅ SQLAlchemy ORM configuration  
✅ Database connection and initialization  
✅ Environment-based configuration  
✅ Basic error handling and logging  
✅ Health check endpoint  
✅ CORS configuration for frontend  
✅ Security headers  
✅ Virtual environment setup  

## Development

### Running Tests
```bash
pytest
```

### Code Quality
```bash
flake8 .
black .
```

### Database Operations
```bash
# The application automatically creates tables on startup
# For manual database operations (future):
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Security Features

- CORS configuration for frontend communication
- Security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
- SQL injection prevention via SQLAlchemy ORM
- Input validation via Marshmallow schemas
- Environment-specific security settings

## Architecture Notes

This backend implementation follows Flask best practices:

- **Application Factory Pattern**: Enables configuration flexibility and testing
- **Blueprint Organization**: Modular route organization for scalability
- **Service Layer**: Business logic separation from route handlers
- **Configuration Management**: Environment-specific settings
- **Error Handling**: Consistent error responses and logging
- **Database Abstraction**: SQLAlchemy ORM for database independence