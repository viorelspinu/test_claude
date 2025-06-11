"""
API routes package for the Todo application.

This package contains Flask blueprint definitions for handling HTTP requests.
Routes define the API endpoints and delegate business logic to service classes.
"""

from .todos import todos_bp