"""
Application factory module.

This module contains the application factory function that creates and configures
the Flask application instance. It initializes all extensions, registers blueprints,
and sets up the application context.

Exports:
    create_app: Factory function that returns a configured Flask application instance
    db: SQLAlchemy database instance
    login_manager: Flask-Login manager instance
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel
from config import Config

# Create extensions instances first
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
babel = Babel()

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: A configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app)

    # Enable Jinja2 extensions
    app.jinja_env.add_extension('jinja2.ext.i18n')

    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.app_context():
        from app.routes import auth, main, admin, profile, news
        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(profile.bp)
        app.register_blueprint(news.bp)

        # Create all tables
        db.create_all()

    return app
