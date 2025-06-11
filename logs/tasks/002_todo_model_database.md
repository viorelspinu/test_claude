# Task 002: Create Todo Model and Database

## Objective
Create Todo data model using SQLAlchemy and set up SQLite database.

## Requirements
1. Create `models.py` with Todo model
2. Configure SQLAlchemy in Flask app
3. Set up SQLite database
4. Initialize database tables

## Todo Model Schema
- id: Primary key, integer, auto-increment
- text: Todo text content, string, required
- completed: Boolean flag, default False
- created_at: Timestamp, default current time

## Expected Deliverables
- `/backend/models.py` - Todo model definition
- Updated `/backend/app.py` - SQLAlchemy configuration
- SQLite database file created
- Database tables initialized

## Success Criteria
- Todo model can be imported and used
- Database connection works
- Tables created successfully
- Ready for CRUD operations