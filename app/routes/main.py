"""
Main routes module.

This module handles the main routes of the application, including the home page,
blog posts, and general content pages. It manages post creation, viewing,
editing, and deletion.

Routes:
    - /: Home page
    - /posts: List all posts
    - /post/<id>: View specific post
    - /post/create: Create new post
    - /post/<id>/edit: Edit existing post
    - /post/<id>/delete: Delete post
"""

import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_required, current_user
from app.models import Post, Comment, Category, Permission
from app import db
from sqlalchemy import func


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Render the home page with recent posts.

    Returns:
        rendered_template: The home page with recent posts
    """
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('main/index.html', posts=posts)

@bp.route('/post/<int:post_id>')
def post(post_id):
    """
    Display a specific post and its comments.

    Args:
        post_id: The ID of the post to display

    Returns:
        rendered_template: The post page with post content and comments
    """
    post = Post.query.get_or_404(post_id)
    # Get comment count using a subquery
    comment_count = Comment.query.filter_by(post_id=post_id).count()
    return render_template('main/post.html',
                         title=post.title,
                         post=post,
                         comment_count=comment_count)

@bp.route('/post/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Create a new post.

    Returns:
        GET: render_template with the create post form
        POST: redirect to the new post's page
    """
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
        return redirect(url_for('main.post', post_id=post.id))
    
    return render_template('main/create_post.html', 
                         categories=categories, 
                         Permission=Permission)

@bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    """
    Add a comment to a post.

    Args:
        post_id: The ID of the post to comment on

    Returns:
        redirect: Redirects to the post page after adding comment
    """
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    
    if content:
        comment = Comment(content=content, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added!', 'success')
    
    return redirect(url_for('main.post', post_id=post_id))

@bp.route('/comment/<int:id>/delete', methods=['POST'])
@login_required
def delete_comment(id):
    """
    Delete a comment.

    Args:
        id (int): The ID of the comment to delete

    Returns:
        redirect: Redirect to the post page after successful comment deletion
    """
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
    """
    Delete a post.

    Args:
        id (int): The ID of the post to delete

    Returns:
        redirect: Redirect to the home page after successful post deletion
    """
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
    """
    Edit a post.

    Args:
        id (int): The ID of the post to edit

    Returns:
        redirect: Redirect to the post page after successful post update
    """
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
    """
    Set the language for the application.

    Args:
        lang_code (str): The language code to set

    Returns:
        redirect: Redirect to the previous page or home page
    """
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