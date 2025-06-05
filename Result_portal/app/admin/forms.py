# Placeholder for admin forms

from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    SelectField, 
    SubmitField, 
    FloatField, 
    TextAreaField, 
    BooleanField,
    PasswordField,  # Was missing
    IntegerField,
    DateField,
    HiddenField
)
from wtforms.validators import DataRequired, Optional, Length, Email, ValidationError, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed  # Was missing
from app.models import Program, Level
import datetime


def coerce_int_or_empty(value):
    if value == '' or value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def get_academic_years(num_years=5):
    """Generate academic years dynamically starting from current year"""
    current_year = datetime.datetime.now().year
    academic_years = []
    
    for i in range(num_years):
        year_start = current_year - i
        year_end = year_start + 1
        academic_year = f"{year_start}-{year_end}"
        academic_years.append((academic_year, academic_year))
    
    return academic_years

class EnterResultForm(FlaskForm):
    program = SelectField('Program', coerce=int, validators=[DataRequired()])
    level = SelectField('Level', coerce=int, validators=[DataRequired()])
    student = SelectField('Student', coerce=int, validators=[Optional()])
    course = SelectField('Course', coerce=int, validators=[DataRequired()])
    semester = SelectField('Semester', choices=[('1', 'First Semester'), ('2', 'Second Semester')], validators=[DataRequired()])
    academic_year = SelectField('Academic Year', choices=get_academic_years(), validators=[DataRequired()])
    score = FloatField('Score', validators=[DataRequired()])
    remarks = TextAreaField('Remarks', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Submit Result')

class UploadResultsForm(FlaskForm):
    file = FileField('Results File', validators=[DataRequired()])
    submit = SubmitField('Upload')

class ManageStudentForm(FlaskForm):
    index_number = StringField('Index Number')
    full_name = StringField('Full Name')
    program = SelectField('Program', choices=[], coerce=str)
    level = SelectField('Level', choices=[('', 'All'), ('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')])
    status = SelectField('Status', choices=[('all', 'All'), ('active', 'Active'), ('archived', 'Archived')], default='active')
    submit = SubmitField('Filter')

    def __init__(self, *args, **kwargs):
        super(ManageStudentForm, self).__init__(*args, **kwargs)
        # Get all active programs
        self.program.choices = [(p.name, p.name) for p in Program.query.filter_by(archived=False).order_by(Program.name).all()]
        # Add an empty choice for "All"
        self.program.choices.insert(0, ('', 'All'))
        # Initialize the form with the current filter values
        self.program.data = kwargs.get('program', '')
        self.level.data = kwargs.get('level', '')
        self.status.data = kwargs.get('status', 'active')

class EditStudentForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    program = SelectField('Program', choices=[], coerce=str, validators=[DataRequired()])
    level = SelectField('Level', choices=[], coerce=str, validators=[DataRequired()])
    submit = SubmitField('Update Student')

    def __init__(self, *args, **kwargs):
        super(EditStudentForm, self).__init__(*args, **kwargs)
        # Get all active programs
        self.program.choices = [(p.name, p.name) for p in Program.query.filter_by(archived=False).order_by(Program.name).all()]
        # Get all active levels
        self.level.choices = [(l.name, l.name) for l in Level.query.filter_by(archived=False).order_by(Level.name).all()]
        # If student is provided, set initial values
        student = kwargs.get('student')
        if student:
            self.full_name.data = student.full_name
            # Handle program
            if student.program_id:
                program = Program.query.get(student.program_id)
                if program:
                    self.program.data = program.name
            else:
                self.program.data = ''
            # Handle level
            if student.level_id:
                level = Level.query.get(student.level_id)
                if level:
                    self.level.data = level.name
            else:
                self.level.data = ''

from wtforms.validators import Optional

class AddEditStudentForm(FlaskForm):
    index_number = StringField('Index Number', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    program = SelectField('Program', coerce=int, validators=[DataRequired()])
    level = SelectField('Level', coerce=str, validators=[DataRequired()])
    username = StringField('Username', validators=[Optional()])
    password = PasswordField('Password', validators=[Optional()])
    submit = SubmitField('Submit')
    
    def __init__(self, *args, **kwargs):
        super(AddEditStudentForm, self).__init__(*args, **kwargs)
        # Get all active programs
        self.program.choices = [(p.id, p.name) for p in Program.query.filter_by(archived=False).order_by(Program.name).all()]
        # Set level choices
        self.level.choices = [('100', '100'), ('200', '200'), ('300', '300'), ('400', '400')]
        
        # Set initial values if provided
        if 'program' in kwargs:
            self.program.data = kwargs['program']
        if 'level' in kwargs:
            self.level.data = str(kwargs['level'])

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

class StudentSearchForm(FlaskForm):
    index_number = StringField('Index Number', validators=[Optional()])
    full_name = StringField('Full Name', validators=[Optional()])
    program = SelectField('Program', coerce=int, choices=[], validators=[Optional()])
    level = SelectField('Level', coerce=int, choices=[], validators=[Optional()])
    status = SelectField('Status', choices=[('', 'All'), ('active', 'Active'), ('archived', 'Archived')], validators=[Optional()])
    submit = SubmitField('Search')
