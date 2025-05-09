# Placeholder for admin forms

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField, FloatField, TextAreaField, PasswordField
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired
from wtforms import TextAreaField, SelectField


class EnterResultForm(FlaskForm):
    index_number = StringField('Student Index Number', validators=[DataRequired()])
    course_code = StringField('Course Code', validators=[DataRequired()])
    score = FloatField('Score', validators=[DataRequired()])
    semester = StringField('Semester', validators=[DataRequired()])
    academic_year = StringField('Academic Year', validators=[DataRequired()])
    remarks = TextAreaField('Remarks')
    submit = SubmitField('Submit Result')

class UploadResultsForm(FlaskForm):
    file = FileField('Results File', validators=[DataRequired()])
    submit = SubmitField('Upload')

from wtforms import SelectField

class ManageStudentForm(FlaskForm):
    index_number = StringField('Index Number')
    full_name = StringField('Full Name')
    program = StringField('Program')
    level = SelectField('Level', choices=[('', 'All'), ('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')])
    status = SelectField('Status', choices=[('all', 'All'), ('active', 'Active'), ('archived', 'Archived')], default='active')
    submit = SubmitField('Filter')

class AddEditStudentForm(FlaskForm):
    index_number = StringField('Index Number', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    program = StringField('Program', validators=[DataRequired()])
    level = SelectField('Level', choices=[('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ResetStudentPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset Password')

class SendNotificationForm(FlaskForm):
    student = SelectField('Student', coerce=int, validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Notification')

class BroadcastMessageForm(FlaskForm):
    program = StringField('Program (optional)')
    level = SelectField('Level (optional)', choices=[('', 'All'), ('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Broadcast Message')

class AddCourseForm(FlaskForm):
    course_code = StringField('Course Code', validators=[DataRequired()])
    course_title = StringField('Course Title', validators=[DataRequired()])
    credit_hours = StringField('Credit Hours', validators=[DataRequired()])
    submit = SubmitField('Add Course')
