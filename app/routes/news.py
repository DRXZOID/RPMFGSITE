"""
News routes module.

This module handles all news-related routes including creating,
viewing, editing, and deleting news articles.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import News
from app.forms import NewsForm
from app import db

bp = Blueprint('news', __name__, url_prefix='/news')

@bp.route('/')
def index():
    """Display all news articles."""
    news_list = News.query.order_by(News.created_at.desc()).all()
    return render_template('news/index.html', news_list=news_list)

@bp.route('/<int:news_id>')
def view(news_id):
    """Display a specific news article."""
    news = News.query.get_or_404(news_id)
    return render_template('news/view.html', news=news)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new news article."""
    form = NewsForm()
    if form.validate_on_submit():
        news = News(
            title=form.title.data,
            content=form.content.data,
            subject=form.subject.data,
            author=current_user
        )
        db.session.add(news)
        db.session.commit()
        flash('News article has been created!', 'success')
        return redirect(url_for('news.view', news_id=news.id))
    return render_template('news/create.html', form=form)

@bp.route('/<int:news_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(news_id):
    """Edit an existing news article."""
    news = News.query.get_or_404(news_id)
    if news.author != current_user:
        flash('You can only edit your own news articles.', 'danger')
        return redirect(url_for('news.view', news_id=news.id))
    
    form = NewsForm()
    if form.validate_on_submit():
        news.title = form.title.data
        news.content = form.content.data
        news.subject = form.subject.data
        db.session.commit()
        flash('News article has been updated!', 'success')
        return redirect(url_for('news.view', news_id=news.id))
    elif request.method == 'GET':
        form.title.data = news.title
        form.content.data = news.content
        form.subject.data = news.subject
    return render_template('news/edit.html', form=form, news=news)

@bp.route('/<int:news_id>/delete', methods=['POST'])
@login_required
def delete(news_id):
    """Delete a news article."""
    news = News.query.get_or_404(news_id)
    if news.author != current_user:
        flash('You can only delete your own news articles.', 'danger')
        return redirect(url_for('news.view', news_id=news.id))
    
    db.session.delete(news)
    db.session.commit()
    flash('News article has been deleted!', 'success')
    return redirect(url_for('news.index')) 