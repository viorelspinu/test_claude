#!/usr/bin/env python3
"""
Management script for Flask application.

This script provides database management commands using Flask-Migrate.
"""

import os
import sys
from flask.cli import FlaskGroup
from app import create_app, db
from app.models import Todo

# Create Flask application
app = create_app()

# Create Flask CLI group
cli = FlaskGroup(app)

@cli.command()
def init_db():
    """Initialize the database with migrations."""
    print("Initializing database...")
    try:
        # This will create all tables based on models
        db.create_all()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

@cli.command()
def seed_db():
    """Seed the database with sample data."""
    print("Seeding database with sample data...")
    try:
        # Create some sample todos for testing
        sample_todos = [
            Todo(
                title="Complete project documentation",
                description="Write comprehensive API docs and user guide",
                priority="high",
                due_date="2024-12-31"
            ),
            Todo(
                title="Review code changes",
                description="Review the latest pull request",
                priority="medium"
            ),
            Todo(
                title="Update dependencies",
                description="Update all npm and pip packages",
                priority="low"
            )
        ]
        
        for todo in sample_todos:
            db.session.add(todo)
        
        db.session.commit()
        print(f"Added {len(sample_todos)} sample todos to database!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.session.rollback()
        sys.exit(1)

@cli.command()
def test_db():
    """Test database connectivity and model operations."""
    print("Testing database connection and model operations...")
    try:
        # Test database connection
        from sqlalchemy import text
        result = db.session.execute(text('SELECT 1'))
        print("✓ Database connection successful")
        
        # Test Todo model creation
        test_todo = Todo(
            title="Test Todo",
            description="This is a test todo item",
            priority="medium"
        )
        db.session.add(test_todo)
        db.session.commit()
        print("✓ Todo model creation successful")
        
        # Test Todo model retrieval
        retrieved_todo = Todo.query.filter_by(title="Test Todo").first()
        if retrieved_todo:
            print("✓ Todo model retrieval successful")
            print(f"  Retrieved: {retrieved_todo}")
        
        # Test Todo model conversion to dict
        todo_dict = retrieved_todo.to_dict()
        print("✓ Todo model serialization successful")
        print(f"  Serialized: {todo_dict}")
        
        # Clean up test data
        db.session.delete(retrieved_todo)
        db.session.commit()
        print("✓ Todo model deletion successful")
        
        print("\nAll database tests passed!")
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        db.session.rollback()
        sys.exit(1)

if __name__ == '__main__':
    cli()