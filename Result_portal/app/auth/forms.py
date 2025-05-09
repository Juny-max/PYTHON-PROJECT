# Placeholder for auth forms

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    index_number = StringField('Index Number', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    program = StringField('Program', validators=[DataRequired()])
    level = StringField('Level', validators=[DataRequired()])
    submit = SubmitField('Register')
