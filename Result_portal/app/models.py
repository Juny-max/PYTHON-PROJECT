from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.Enum('admin', 'student', name='user_types'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    student = db.relationship('Student', backref='user', uselist=False, lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.user_type == 'admin'

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    index_number = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    program = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    results = db.relationship('Result', backref='student', lazy=True)
    
    def calculate_gpa(self, semester=None, academic_year=None):
        results = self.results
        if semester:
            results = [r for r in results if r.semester == semester]
        if academic_year:
            results = [r for r in results if r.academic_year == academic_year]
            
        if not results:
            return 0.0
            
        total_credit_points = 0
        total_credit_hours = 0
        
        grade_points = {
            'A': 4.0, 'B+': 3.5, 'B': 3.0, 'C+': 2.5,
            'C': 2.0, 'D+': 1.5, 'D': 1.0, 'F': 0.0
        }
        
        for result in results:
            points = grade_points.get(result.grade, 0.0)
            total_credit_points += points * result.course.credit_hours
            total_credit_hours += result.course.credit_hours
        
        return round(total_credit_points / total_credit_hours, 2) if total_credit_hours else 0.0

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    credit_hours = db.Column(db.Integer, nullable=False)
    results = db.relationship('Result', backref='course', lazy=True)

class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    score = db.Column(db.Numeric(5, 2), nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    remarks = db.Column(db.Text)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def determine_grade(self):
        score = float(self.score)
        if score >= 80:
            return 'A'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'C+'
        elif score >= 60:
            return 'C'
        elif score >= 55:
            return 'D+'
        elif score >= 50:
            return 'D'
        else:
            return 'F'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))