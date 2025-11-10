"""
Application entry point.

This module initializes and runs the Flask application using the factory pattern.
It serves as the main entry point for starting the web server.
"""

from flask_migrate import Migrate
from app import create_app, db

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
