"""
Flask extensions initialization

This module initializes Flask extensions that need to be shared across the application.
Separating extensions helps avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()