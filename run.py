"""
Application entry point.

This module initializes and runs the Flask application using the factory pattern.
It serves as the main entry point for starting the web server.
"""

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
