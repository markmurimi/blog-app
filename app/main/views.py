from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from datetime import datetime, timezone
from .. import db
from ..models import User, Blog, Comment
from flask_login import login_required, current_user
from .forms import BlogForm, CommentForm

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def single_line(id):
    article = Blog.query.get(id)
    title = "article"
    comments = Comment.get_comments(id)

    return render_template('blog.html', article=article, title=title, comments=comments)
@main.route('/')
def index():
    title = 'Home'
    posts = Blog.get_posts()
    print(posts)
    return render_template('index.html', title=title, posts=posts)

@main.route('/new/blog', methods=['GET', 'POST'])
def new_blog():
    '''
    This is the route to create new post
    '''
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        blog = form.blog.data
        new_blog = Blog(title=title, blog=blog)
        new_blog.save_blog()
        return redirect(url_for('main.index'))
    return render_template('new_blog.html', form=form)


#delete selected comment
@main.route('/delete/comment/<int:id>', methods=['GET', 'POST'])
def delete_selected_comment(id):
    """
    Route to delete a comment
    """
    comment = Comment.query.get(id)
    comment.delete_comment(id)

    return redirect(url_for('main.index'))

@main.route('/post/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_comment(id):
    post = Blog.query.filter_by(id=id).first()

    if post is None:
        abort(404)

    form = CommentForm()

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comment(
            opinion=opinion, articles_id=id, user_id=current_user.id)
        new_comment.save_comment()

        return redirect(url_for('main.index'))

    title = 'New Comment'
    return render_template('new_comment.html', title=title, comment_form=form)
