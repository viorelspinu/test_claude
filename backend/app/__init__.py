"""
Flask Todo Application

A RESTful API for managing todo tasks built with Flask and SQLAlchemy.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """
    Application factory function to create and configure Flask app
    
    Args:
        config_name (str): Configuration name (development, production, testing)
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///todo_app.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Import models to register them with SQLAlchemy
    from app import models
    
    # Register blueprints (API routes will be added in later tasks)
    # from app.api import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')
    
    return app


# Make db available at module level for convenience
__all__ = ['create_app', 'db']