"""
Authentication routes module.

This module handles user authentication including login, logout, registration,
and password reset functionality. It manages user sessions and security.

Routes:
    - /login: User login
    - /logout: User logout
    - /register: New user registration
    - /reset-password: Password reset
    - /confirm-email: Email confirmation
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    Returns:
        rendered_template: Login form on GET, redirects on successful POST
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """
    Handle user logout.

    Returns:
        redirect: Redirects to home page after logging out
    """
    logout_user()
    return redirect(url_for('main.index')) 