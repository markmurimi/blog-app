from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..models import User, Post, Comments
from flask_login import login_required, current_user
from datetime import datetime, timezone
from .. import db


# Views index
@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home'
    posts = Post.get_posts()
    return render_template('index.html', title=title, posts=posts)

# view function to render a selected article and its comments


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def single_line(id):
    '''
    View function to return a single article
    '''
    post = Post.query.get(id)
    title = "article"
    comments = Comment.get_comments(id)

    return render_template('single-post.html', article=article, title=title, comments=comments)

# view route to post a post


@main.route('/new/post', methods=['GET', 'POST'])
def new_post():
    '''
    route to avail form for writing a new post
    '''
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        new_post = Post(title=title, post=post)
        new_post.save_post()
        return redirect(url_for('main.index'))
    return render_template('new_post.html', form=form)

#delete articles


@main.route('/delete/post/<int:id>', methods=['GET', 'POST'])
def delete_post(id):
    """
    view route to delete a selected post
    """
    article = Post.query.filter_by(id=id).first()

    if article is None:
        abort(404)

    article.delete_post()
    return redirect(url_for('main.index'))

#commenting route


@main.route('/post/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_comment(id):
    '''
    View new comment function that returns a page with a form to create a comment for the specified post
    '''
    post = Post.query.filter_by(id=id).first()

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

#delete selected comment


@main.route('/delete/comment/<int:id>', methods=['GET', 'POST'])
def delete_selected_comment(id):
    """
    view route to delete a selected comment
    """
    comment = Comment.query.get(id)
    comment.delete_comment(id)

    return redirect(url_for('main.index'))
