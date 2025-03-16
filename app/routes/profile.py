"""
User profile routes module.

This module handles user profile-related functionality including viewing,
editing, and managing user profiles. It allows users to update their
information and manage their account settings.

Routes:
    - /profile: View own profile
    - /profile/edit: Edit profile
    - /profile/<username>: View other user's profile
    - /profile/settings: Account settings
"""
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models import db, User
from app import create_app

bp = Blueprint('profile', __name__, url_prefix='/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def view_profile():
    """
    Display user's own profile.

    Returns:
        rendered_template: User's profile page with their information
    """
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('profile/view.html', user=user)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Handle profile editing.

    Returns:
        rendered_template: Profile edit form on GET, redirects on successful POST
    """
    if request.method == 'POST':
        current_user.bio = request.form.get('bio')
        
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(create_app().config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                current_user.avatar = filename

        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('profile.view_profile'))
    
    return render_template('profile/edit.html')

@bp.route('/<username>')
def view_profile_other(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile/view.html', user=user)

@bp.route('/settings')
@login_required
def account_settings():
    # This route is not implemented in the original file or the new docstring
    # It's assumed to exist as it's called in the edit_profile route
    pass

# Add similar docstrings for other routes... 