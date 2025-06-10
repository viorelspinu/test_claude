"""
API Blueprint Module

This module defines the API blueprint for the Flask Todo application.
All API routes are registered under the /api prefix.
"""

from flask import Blueprint

# Create the API blueprint
api_bp = Blueprint('api', __name__)

# Import routes to register them with the blueprint
from app.api import routes

__all__ = ['api_bp']