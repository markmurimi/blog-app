from . import db
from flask_login import UserMixin
from . import login_manager
from sqlalchemy.sql import func



class User(UserMixin,db.Model):
    """ class modelling the users """

    __tablename__='users'

    #create the columns
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True, index =True)
    password_hash = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    posts = db.relationship("Post", backref="user", lazy = "dynamic")
    comment = db.relationship("Comments", backref="user", lazy = "dynamic")

class Post(db.Model):
    """ List of pitches in each category """

    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship("Comments", backref="pitches", lazy = "dynamic")

    def save_post(self):
        ''' Save the posts '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        Post.all_posts.clear()

    def get_posts(id):
        pitches = Pitch.query.filter_by(category_id=id).all()
        return pitches
