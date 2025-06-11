# Task: Create Todo Data Model and Database Schema

**Task ID:** task-003-todo-model-schema

## Description

Define the Todo SQLAlchemy model with all required fields, constraints, and create the database migration.

## Type
Backend

## Dependencies
- task-002-backend-core-setup (Flask application core and database connection)

## Estimated Time
1.5 hours

## Acceptance Criteria

- [ ] Todo model with all required fields (id, title, description, priority, status, due_date, timestamps)
- [ ] Proper field validations and constraints
- [ ] Database indexes created for performance
- [ ] Migration script generated and executed
- [ ] Model can be imported and used in Python

## Deliverables

- `/backend/app/models/todo.py` with Todo model class
- Database migration files
- Database created with todos table

## Test Requirements

- [ ] Model creation and validation works
- [ ] Database schema matches requirements  
- [ ] Indexes are properly created

## Detailed Requirements

### Todo Model Fields

1. **id** - Primary key (auto-incrementing integer)
2. **title** - String field (required, max 200 characters)
3. **description** - Text field (optional, unlimited length)
4. **priority** - Enum field (low, medium, high) with default 'medium'
5. **status** - Enum field (pending, completed) with default 'pending'
6. **due_date** - Date field (optional)
7. **created_at** - Timestamp (auto-generated on creation)
8. **updated_at** - Timestamp (auto-updated on modification)

### Constraints and Validations

- Title field must not be empty when provided
- Priority must be one of: 'low', 'medium', 'high'
- Status must be one of: 'pending', 'completed'
- Due date must be in the future or today (validation at application level)

### Database Indexes

- Index on status field for filtering queries
- Index on due_date field for overdue calculations
- Index on created_at field for sorting
- Composite index on (status, due_date) for common queries

### Migration Requirements

- Create database migration using Flask-Migrate
- Ensure migration can be applied and rolled back cleanly
- Include all indexes in the migration script

## Success Criteria

The task is complete when:
1. Todo model is properly defined with all fields and constraints
2. Database migration has been created and executed successfully
3. All required indexes are created and functional
4. Model can be imported and used in Python applications
5. Database schema matches the specification exactly