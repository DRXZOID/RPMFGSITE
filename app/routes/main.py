from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Post, Comment, Category, Permission
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('main/index.html', posts=posts, Permission=Permission)

@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('main/post.html', post=post, Permission=Permission)

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
    if current_user == comment.author or current_user.has_permission(Permission.MODERATE):
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('main.post', id=comment.post_id))

# Add this context processor to make Permission available to all templates
@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission) 