import email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField, ValidationError,BooleanField
from wtforms.validators import InputRequired,Email,EqualTo
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password_confirm', message='Passwords are not the same')])
    password_confirm = PasswordField('Confirm Your Password', validators=[InputRequired()])
    submit = SubmitField('Register here')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError('An account already exists with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('A user already exist with that username')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(),Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Save Details')
    submit = SubmitField('Sign In')
