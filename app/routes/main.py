from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_required, current_user
from app.models import Post, Comment, Category, Permission
from app import db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('main/index.html', posts=posts)

@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('main/post.html', 
                         post=post, 
                         Comment=Comment,  # Pass the Comment model
                         Permission=Permission)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if not current_user.has_permission(Permission.WRITE):
        flash('You do not have permission to create posts.')
        return redirect(url_for('main.index'))
    
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        
        if not all([title, content, category_id]):
            flash('Please fill out all required fields.')
            return render_template('main/create_post.html', categories=categories)
        
        post = Post(title=title, content=content, 
                   author=current_user, 
                   category_id=category_id)
        
        # Handle image upload if present
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post.image_url = filename
        
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!')
        return redirect(url_for('main.post', id=post.id))
    
    return render_template('main/create_post.html', 
                         categories=categories, 
                         Permission=Permission)

@bp.route('/post/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    if not current_user.has_permission(Permission.COMMENT):
        flash('You do not have permission to comment.')
        return redirect(url_for('main.post', id=id))
    
    content = request.form.get('content')
    if not content:
        flash('Comment cannot be empty.')
        return redirect(url_for('main.post', id=id))
    
    post = Post.query.get_or_404(id)
    comment = Comment(content=content, author=current_user, post=post)
    db.session.add(comment)
    db.session.commit()
    flash('Your comment has been added.')
    return redirect(url_for('main.post', id=id))

@bp.route('/comment/<int:id>/delete', methods=['POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if not current_user.is_admin and current_user.id != comment.author.id:
        flash('You do not have permission to delete this comment.')
        return redirect(url_for('main.post', id=comment.post_id))
    
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.')
    return redirect(url_for('main.post', id=post_id))

@bp.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if not current_user.is_admin and current_user.id != post.author.id:
        flash('You do not have permission to delete this post.')
        return redirect(url_for('main.post', id=id))
    
    # Delete associated comments first
    Comment.query.filter_by(post_id=id).delete()
    
    # Delete the post
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.')
    return redirect(url_for('main.index'))

@bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    # Check if user has permission to edit
    if not current_user.is_admin and current_user.id != post.author.id:
        flash('You do not have permission to edit this post.')
        return redirect(url_for('main.post', id=id))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        
        if not all([title, content, category_id]):
            flash('Please fill out all required fields.')
            return redirect(url_for('main.edit_post', id=id))
        
        post.title = title
        post.content = content
        post.category_id = category_id
        
        # Handle image upload if present
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                if allowed_file(file.filename):
                    # Delete old image if it exists
                    if post.image_url:
                        try:
                            old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], post.image_url)
                            if os.path.exists(old_image_path):
                                os.remove(old_image_path)
                        except Exception as e:
                            current_app.logger.error(f"Error deleting old image: {e}")
                    
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    post.image_url = filename
                else:
                    flash('Invalid file type.')
                    return redirect(url_for('main.edit_post', id=id))
        
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('main.post', id=id))
    
    categories = Category.query.all()
    return render_template('main/edit_post.html', post=post, categories=categories)

@bp.route('/language/<lang_code>')
def set_language(lang_code):
    # Validate language code
    if lang_code in ['en', 'ua', 'ru']:
        session['language'] = lang_code
    return redirect(request.referrer or url_for('main.index'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add this context processor to make models available to all templates
@bp.app_context_processor
def inject_models():
    return dict(
        Comment=Comment,
        Permission=Permission
    ) 