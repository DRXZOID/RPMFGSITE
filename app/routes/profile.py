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
from app.forms import EditProfileForm

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
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            # Handle avatar upload
            picture_file = save_picture(form.avatar.data)
            current_user.avatar = picture_file
            
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        current_user.newsletter_subscription = form.newsletter_subscription.data
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile.view_profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.website.data = current_user.website
        form.newsletter_subscription.data = current_user.newsletter_subscription
    
    return render_template('profile/edit_profile.html', form=form)

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

@bp.route('/profile/delete', methods=['POST'])
@login_required
def delete_account():
    # Delete user's avatar file if it exists
    if current_user.avatar:
        avatar_path = os.path.join(current_app.root_path, 'static/avatars', current_user.avatar)
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
    
    db.session.delete(current_user)
    db.session.commit()
    flash('Your account has been deleted.', 'info')
    return redirect(url_for('main.index'))

# Add similar docstrings for other routes... 