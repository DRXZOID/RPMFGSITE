from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Post, Category, db, Comment
from app.models import Permission

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=10)
    categories = Category.query.all()
    return render_template('main/index.html', posts=posts, categories=categories)

@bp.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('main/post.html', post=post)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        
        post = Post(title=title, content=content, 
                   author=current_user, 
                   category_id=category_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post', id=post.id))
    
    categories = Category.query.all()
    return render_template('main/create_post.html', categories=categories)

@bp.route('/post/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    if not current_user.has_permission(Permission.COMMENT):
        flash('You do not have permission to comment.')
        return redirect(url_for('main.post', id=id))
    
    post = Post.query.get_or_404(id)
    content = request.form.get('content')
    if content:
        comment = Comment(content=content, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('main.post', id=id))

@bp.route('/comment/<int:id>/delete', methods=['POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user == comment.author or current_user.has_permission(Permission.MODERATE):
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for('main.post', id=comment.post_id)) 