# Placeholder for admin forms

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired

class UploadResultsForm(FlaskForm):
    file = FileField('Results File', validators=[DataRequired()])
    submit = SubmitField('Upload')

class ManageStudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    submit = SubmitField('Search')
