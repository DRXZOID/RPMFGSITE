"""
Database models module.
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(UserMixin, db.Model):
    """
    User model for storing user account information.
    
    Attributes:
        id: Primary key
        username: User's display name
        email: User's email address
        password_hash: Hashed password
        bio: User's biography or description
        avatar: Profile picture filename
        location: User's location
        website: User's personal website
        newsletter_subscription: Newsletter opt-in status
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # New profile fields
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(20))
    location = db.Column(db.String(100))
    website = db.Column(db.String(200))
    newsletter_subscription = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_permission(self, permission):
        # If user is admin, they have all permissions
        if self.is_admin:
            return True
        # If user has no role, they have no permissions
        if self.role is None:
            return False
        # Check if the user's role has the requested permission
        return (self.role.permissions & permission) == permission

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Permission(db.Model):
    """
    Permission model for defining user access levels.
    
    Attributes:
        id (int): Primary key for the permission
        name (str): Name of the permission
        description (str): Description of what the permission allows
        created_at (datetime): Timestamp of when the permission was created
        updated_at (datetime): Timestamp of when the permission was last updated
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Category(db.Model):
    """
    Category model for organizing posts.
    
    Attributes:
        id (int): Primary key for the category
        name (str): Name of the category (unique)
        description (str): Optional description of the category
        created_at (datetime): Timestamp of when the category was created
        updated_at (datetime): Timestamp of when the category was last updated
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define the relationship here only
    posts = db.relationship('Post', backref='category', lazy=True)

class Post(db.Model):
    """
    Post model for blog posts or articles.
    
    Attributes:
        id (int): Primary key for the post
        title (str): Title of the post
        content (str): Main content of the post
        created_at (datetime): Timestamp of when the post was created
        updated_at (datetime): Timestamp of when the post was last updated
        author_id (int): Foreign key to the User model
        category_id (int): Foreign key to the Category model
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # Remove the category relationship since it's defined in Category model
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')

class Comment(db.Model):
    """
    Comment model for post comments.
    
    Attributes:
        id (int): Primary key for the comment
        content (str): Content of the comment
        created_at (datetime): Timestamp of when the comment was created
        updated_at (datetime): Timestamp of when the comment was last updated
        author_id (int): Foreign key to the User model
        post_id (int): Foreign key to the Post model
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

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

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(128), nullable=False)
    details = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='activities')

class News(db.Model):
    """
    News model for storing news articles.
    
    Attributes:
        id: Primary key
        title: News article title
        content: Main content of the news article
        subject: Subject/category of the news
        author_id: ID of the user who created the news
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    author = db.relationship('User', backref='news_articles') 