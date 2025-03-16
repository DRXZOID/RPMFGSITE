from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Category, db, Role, Permission
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
    return render_template('admin/dashboard.html')

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