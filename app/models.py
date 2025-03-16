from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    avatar = db.Column(db.String(200))
    bio = db.Column(db.Text)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        return self.role is not None and (self.role.permissions & permission) == permission

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    posts = db.relationship('Post', backref='category', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    image_url = db.Column(db.String(200))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

# Add permissions constants
class Permission:
    READ = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

def init_roles():
    roles = {
        'User': [Permission.READ, Permission.COMMENT],
        'Moderator': [Permission.READ, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
        'Admin': [Permission.READ, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN]
    }
    
    for role_name, role_permissions in roles.items():
        role = Role.query.filter_by(name=role_name).first()
        if role is None:
            role = Role(name=role_name)
        role.permissions = sum(role_permissions)
        db.session.add(role)
    db.session.commit() 