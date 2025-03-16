from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_babel import Babel
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
babel = Babel()

def create_app():
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
        from app.routes import auth, main, admin, profile
        app.register_blueprint(auth.bp)
        app.register_blueprint(main.bp)
        app.register_blueprint(admin.bp)
        app.register_blueprint(profile.bp)

        # Create all tables
        db.create_all()

    return app 