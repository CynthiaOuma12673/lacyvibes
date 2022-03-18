from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectField
from wtforms.validators import Email, InputRequired

from app import email

class VibeForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    post = TextAreaField('Your  Post', validators=[InputRequired()], render_kw= {'class': 'form-control','rows':5})
    submit = SubmitField('Submit Your Post')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Kindly tell us about yourself', validators=[InputRequired()])
    submit = SubmitField('Save Bio')

class CommentForm(FlaskForm):
    comment = TextAreaField('Add a comment here', validators=[InputRequired()])
    submit = SubmitField('Comment')

class UpdateVibe(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    post = TextAreaField('Update your Post', validators=[InputRequired()], render_kw={'class':'form-control', 'rows':5})
    submit = SubmitField('Submit Your Post')

class SubscribeForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email()], render_kw={'placeHolder':'Enter email address here....'})
    submit = SubmitField('Subscribe')

