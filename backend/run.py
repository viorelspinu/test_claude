"""
Flask application entry point

Run this file to start the development server.
"""

import os
from app import create_app, db

# Create Flask application
app = create_app()


@app.cli.command()
def init_db():
    """Initialize the database with tables."""
    db.create_all()
    print("Database initialized!")


@app.cli.command()
def reset_db():
    """Reset the database (drop and recreate all tables)."""
    db.drop_all()
    db.create_all()
    print("Database reset!")


if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the development server
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"Starting Flask development server on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )