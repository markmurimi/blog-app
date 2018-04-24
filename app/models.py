from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    '''class modelling the user'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    pasword_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    comment = db.relationship("Comment", backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.username}'


class Blog(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    blog = db.Column(db.String(3000))
    comment = db.relationship("Comment", backref='article', lazy='dynamic')

    def save_blog(self):
        '''
        save a blog in the database
        '''
        db.session.add(self)
        db.session.commit()

    def delete_blog(self):
        '''delete a given blog from the database'''
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_posts(cls):
        '''
        Function that queries the Posts Table in the database and returns all the information from the Posts Table

        Returns:
            posts : all the information in the posts table
        '''
        posts = Blog.query.all()
        return posts


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    opinion = db.Column(db.String)
    articles_id = db.Column(db.Integer, db.ForeignKey(
        "articles.id", ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_comment(self):
        '''
        Function that saves a new comment given as feedback to a post
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comment.query.filter_by(articles_id=id).all()
        return comment

    def delete_comment(cls, comment_id):
        '''
        Function that deletes a specific single comment from the comments table and database
        '''
        comment = Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()
