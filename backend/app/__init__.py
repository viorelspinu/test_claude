"""
Flask Todo Application

A RESTful API for managing todo tasks built with Flask and SQLAlchemy.
"""

from flask import Flask
import os
from app.extensions import db, migrate, cors


def create_app(config_name=None):
    """
    Application factory function to create and configure Flask app
    
    Args:
        config_name (str): Configuration name (development, production, testing)
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS with settings from config
    cors.init_app(
        app, 
        origins=app.config['CORS_ORIGINS'],
        methods=app.config['CORS_METHODS'],
        allow_headers=app.config['CORS_HEADERS'],
        supports_credentials=True
    )
    
    # Import models to register them with SQLAlchemy
    from app import models
    
    # Register blueprints
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix=app.config['API_PREFIX'])
    
    return app


# Make db available at module level for convenience
__all__ = ['create_app', 'db']