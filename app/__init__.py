from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes import auth, main, admin, profile
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(profile.bp)

    with app.app_context():
        # Import models here to avoid circular imports
        from app.models import Role, User, Category, Post, Comment
        
        # Create all tables
        db.create_all()
        
        # Initialize roles after tables are created
        from app.models import init_roles
        init_roles()

    return app 