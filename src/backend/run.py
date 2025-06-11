#!/usr/bin/env python3
"""
Application entry point for the Todo Flask application.

This script creates and runs the Flask application using the factory pattern.
It handles environment configuration and provides a simple way to start the server.
"""

import os
import sys
from app import create_app, db

# Create the Flask application
app = create_app()

if __name__ == '__main__':
    """
    Run the application directly when this script is executed.
    
    Environment variables that can be set:
    - FLASK_ENV: development, testing, or production (default: development)
    - FLASK_HOST: Host to bind to (default: 127.0.0.1)
    - FLASK_PORT: Port to bind to (default: 5000)
    - FLASK_DEBUG: Enable debug mode (default: True in development)
    """
    
    # Get configuration from environment
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Override debug mode based on environment
    if os.environ.get('FLASK_ENV') == 'production':
        debug = False
    
    print(f"Starting Todo Flask application...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print("-" * 50)
    
    try:
        # Ensure database tables exist
        with app.app_context():
            db.create_all()
            print("Database tables created/verified successfully")
        
        # Start the Flask development server
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug,  # Auto-reload on code changes in debug mode
            threaded=True  # Handle multiple requests concurrently
        )
        
    except KeyboardInterrupt:
        print("\nShutting down Todo application...")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        sys.exit(1)