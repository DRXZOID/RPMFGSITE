from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models import db, User
from app import create_app

bp = Blueprint('profile', __name__, url_prefix='/profile')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/<username>')
def view_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile/view.html', user=user)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
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
        return redirect(url_for('profile.view_profile', username=current_user.username))
    
    return render_template('profile/edit.html') 