"""
Flask Application Factory

This module implements the Flask application factory pattern for the Todo application.
It provides proper configuration management, database setup, and error handling.
"""

import logging
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Global database and migration instances
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """
    Application factory function that creates and configures a Flask app instance.
    
    Args:
        config_name (str, optional): Configuration to use ('development', 'testing', 'production')
                                   Defaults to 'development' if not specified.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models for Flask-Migrate to detect them
    from app.models import Todo
    
    # Configure CORS
    CORS(app, origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000"   # Alternative localhost
    ])
    
    # Configure logging
    setup_logging(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints and routes
    register_blueprints(app)
    
    # Note: Database tables are managed via Flask-Migrate
    # Use `flask db upgrade` to create/update database schema
    
    return app


def setup_logging(app):
    """Configure application logging."""
    if not app.debug and not app.testing:
        # Production logging configuration
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Todo application startup')


def register_error_handlers(app):
    """Register application error handlers."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'error': {
                'code': 'BAD_REQUEST',
                'message': 'The request was invalid or malformed',
                'timestamp': db.func.now()
            }
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'The requested resource was not found',
                'timestamp': db.func.now()
            }
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        db.session.rollback()
        app.logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An internal server error occurred',
                'timestamp': db.func.now()
            }
        }), 500
    
    @app.after_request
    def after_request(response):
        """Add security headers to all responses."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response


def register_blueprints(app):
    """Register application blueprints and routes."""
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        """Health check endpoint for monitoring."""
        try:
            # Test database connection
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db_status = 'healthy'
        except Exception as e:
            app.logger.error(f"Database health check failed: {str(e)}")
            db_status = 'unhealthy'
        
        return jsonify({
            'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
            'database': db_status,
            'version': '1.0.0'
        })
    
    # Basic API info endpoint
    @app.route('/api')
    def api_info():
        """API information endpoint."""
        return jsonify({
            'name': 'Todo API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'todos': '/api/todos'
            }
        })
    
    # Register todo routes blueprint
    from .routes.todos import todos_bp
    app.register_blueprint(todos_bp, url_prefix='/api/todos')