from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from .models import Todo
    
    with app.app_context():
        db.create_all()
    
    # Register routes
    from .routes import register_routes
    register_routes(app)
    
    @app.route('/api/health')
    def health():
        return {'status': 'ok', 'message': 'Flask backend running'}
    
    return app