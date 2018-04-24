from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import Required

class CommentForm(FlaskForm):
    '''
    Class to create a comment form using wtf-forms for creating a comments on a post
    '''
    opinion = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    title = StringField('Blog Title', validators=[Required()])
    blog = StringField('Blog', validators=[Required()])
    submit = SubmitField('Post')
