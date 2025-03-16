from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Category, User, Post, Comment, db, Role, Permission, Activity
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def dashboard():
    # Get statistics
    stats = {
        'total_users': User.query.count(),
        'total_posts': Post.query.count(),
        'total_categories': Category.query.count(),
        'total_comments': Comment.query.count()
    }

    # Get recent activities
    recent_activities = Activity.query.order_by(Activity.timestamp.desc()).limit(10).all()

    # Get all users
    users = User.query.all()

    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_activities=recent_activities,
                         users=users)

@bp.route('/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def categories():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully')
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form.get('name')
        db.session.commit()
        flash('Category updated successfully')
        return redirect(url_for('admin.categories'))
    return render_template('admin/edit_category.html', category=category)

@bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully')
    return redirect(url_for('admin.categories'))

@bp.route('/roles', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_roles():
    if request.method == 'POST':
        name = request.form.get('name')
        permissions = 0
        for perm in request.form.getlist('permissions'):
            permissions |= int(perm)
        role = Role(name=name, permissions=permissions)
        db.session.add(role)
        db.session.commit()
    roles = Role.query.all()
    return render_template('admin/roles.html', roles=roles, Permission=Permission)

@bp.route('/roles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_role(id):
    role = Role.query.get_or_404(id)
    if request.method == 'POST':
        role.name = request.form.get('name')
        
        # Reset permissions
        role.permissions = 0
        
        # Update permissions based on form data
        for perm in request.form.getlist('permissions'):
            role.permissions |= int(perm)
        
        db.session.commit()
        
        # Log the activity
        activity = Activity(
            user_id=current_user.id,
            action='Edit role',
            details=f'Updated role: {role.name}'
        )
        db.session.add(activity)
        db.session.commit()
        
        flash('Role updated successfully')
        return redirect(url_for('admin.manage_roles'))
    
    return render_template('admin/edit_role.html', role=role, Permission=Permission)

@bp.route('/roles/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_role(id):
    role = Role.query.get_or_404(id)
    
    # Check if role has any users
    if role.users.count() > 0:
        flash('Cannot delete role with assigned users')
        return redirect(url_for('admin.manage_roles'))
    
    # Log the activity
    activity = Activity(
        user_id=current_user.id,
        action='Delete role',
        details=f'Deleted role: {role.name}'
    )
    
    db.session.delete(role)
    db.session.add(activity)
    db.session.commit()
    
    flash('Role deleted successfully')
    return redirect(url_for('admin.manage_roles'))

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role_id = request.form.get('role_id')
        
        # Check if username already exists
        if username != user.username and User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('admin.edit_user', id=id))
        
        user.username = username
        user.email = email
        user.role_id = role_id
        
        db.session.commit()
        flash('User updated successfully')
        return redirect(url_for('admin.dashboard'))
    
    roles = Role.query.all()
    return render_template('admin/edit_user.html', user=user, roles=roles)

@bp.route('/users/<int:id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash('You cannot deactivate your own account')
        return redirect(url_for('admin.dashboard'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} has been {status}')
    
    # Log the activity
    activity = Activity(
        user_id=current_user.id,
        action=f'Toggle user status',
        details=f'Changed {user.username} status to {status}'
    )
    db.session.add(activity)
    db.session.commit()
    
    return redirect(url_for('admin.dashboard')) 