from . import db
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):

    @login_manager.user_loader
    '''
    This function queries the database and gets a user's id as the response to the query
    '''

    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    """ class modelling the users """

    __tablename__='users'

    #create the columns
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index =True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    comment = db.relationship("Comments", backref="user", lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You can not read the password Attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def _repr_(self):
        return f'User {self.username}'

class Post(db.Model):
    """ List of pitches in each category """

    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    post = db.Column(db.String(3000))
    comment = db.relationship("Comment", backref="posts", lazy = "dynamic")

    def save_post(self):
        ''' Save the posts '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_posts(cls):
        Post.all_posts.clear()

    def get_posts(id):
        pitches = Post.query.filter_by(category_id=id).all()
        return posts

    def delete_post(self):
        '''deleting a post from the database'''
        db.session.delete(self)
        db.session.commit()

    posts = Post.query.order_by(Blog.id.desc()).all() return posts
class Comments(db.Model):
    '''User comment model for each post'''

    __tablename__ = 'comments'

    # add columns
    id = db.Column(db. Integer, primary_key=True)
    opinion = db.Column(db.String(255))
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    posts_id = db.Column(db.Integer, db.ForeignKey("articles.id", ondelete='CASCADE'))

    def save_comment(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(self, id):
        comment = Comments.query.order_by(
            Comments.time_posted.desc()).filter_by(posts_id=id).all()
        return comment

    def delete_comment(cls, comment_id):
        '''
        Function that deletes a specific single comment from the comments table and database

        Args:
            comment_id : specific comment id
        '''
        comment = Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()
