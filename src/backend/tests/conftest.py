"""
Pytest configuration and fixtures for the Todo application tests.

This module provides shared test fixtures and configuration for the test suite.
"""

import pytest
import tempfile
import os
from app import create_app, db
from app.models.todo import Todo, PriorityEnum, StatusEnum
from datetime import date, datetime, timedelta


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False,
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
    
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_todo_data():
    """Sample todo data for testing."""
    return {
        'title': 'Test Todo',
        'description': 'This is a test todo',
        'priority': 'medium',
        'due_date': (date.today() + timedelta(days=7)).isoformat()
    }


@pytest.fixture
def create_sample_todos(app):
    """Create sample todos in the database for testing."""
    with app.app_context():
        todos = [
            Todo(
                title="Completed Todo",
                description="This todo is completed",
                priority=PriorityEnum.HIGH,
                status=StatusEnum.COMPLETED,
                due_date=date.today() - timedelta(days=1)
            ),
            Todo(
                title="Pending Todo",
                description="This todo is pending",
                priority=PriorityEnum.MEDIUM,
                status=StatusEnum.PENDING,
                due_date=date.today() + timedelta(days=5)
            ),
            Todo(
                title="Overdue Todo",
                description="This todo is overdue",
                priority=PriorityEnum.LOW,
                status=StatusEnum.PENDING,
                due_date=date.today() - timedelta(days=3)
            ),
            Todo(
                title="No Due Date Todo",
                description="This todo has no due date",
                priority=PriorityEnum.HIGH,
                status=StatusEnum.PENDING
            )
        ]
        
        for todo in todos:
            db.session.add(todo)
        db.session.commit()
        
        # Return the created todos for test assertions
        return todos