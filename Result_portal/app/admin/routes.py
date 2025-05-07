from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import csv
from datetime import datetime
from app import db
from app.admin import bp
from app.admin.forms import UploadResultsForm, AddCourseForm
from app.models import User, Student, Course, Result
from app.utils import allowed_file

@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    
    total_students = Student.query.count()
    total_courses = Course.query.count()
    recent_results = Result.query.order_by(Result.uploaded_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         title='Admin Dashboard',
                         total_students=total_students,
                         total_courses=total_courses,
                         recent_results=recent_results)

@bp.route('/upload_results', methods=['GET', 'POST'])
@login_required
def upload_results():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    
    form = UploadResultsForm()
    if form.validate_on_submit():
        if form.file.data:
            file = form.file.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    with open(filepath, 'r') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            student = Student.query.filter_by(index_number=row['index_number']).first()
                            course = Course.query.filter_by(code=row['course_code']).first()
                            
                            if not student or not course:
                                continue
                            
                            result = Result(
                                student_id=student.id,
                                course_id=course.id,
                                score=float(row['score']),
                                semester=row['semester'],
                                academic_year=row['academic_year'],
                                uploaded_by=current_user.id
                            )
                            result.grade = result.determine_grade()
                            db.session.add(result)
                        
                        db.session.commit()
                        flash('Results uploaded successfully!', 'success')
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error processing CSV file: {str(e)}', 'danger')
                finally:
                    os.remove(filepath)
            else:
                flash('Only CSV files are allowed', 'danger')
        else:
            # Handle manual form submission
            student = Student.query.filter_by(index_number=form.index_number.data).first()
            course = Course.query.filter_by(code=form.course_code.data).first()
            
            if not student or not course:
                flash('Student or Course not found', 'danger')
                return redirect(url_for('admin.upload_results'))
            
            result = Result(
                student_id=student.id,
                course_id=course.id,
                score=form.score.data,
                semester=form.semester.data,
                academic_year=form.academic_year.data,
                remarks=form.remarks.data,
                uploaded_by=current_user.id
            )
            result.grade = result.determine_grade()
            db.session.add(result)
            db.session.commit()
            flash('Result added successfully!', 'success')
        
        return redirect(url_for('admin.upload_results'))
    
    return render_template('admin/upload_results.html', title='Upload Results', form=form)

@bp.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    
    form = AddCourseForm()
    if form.validate_on_submit():
        course = Course(
            code=form.code.data,
            title=form.title.data,
            credit_hours=form.credit_hours.data
        )
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin.add_course'))
    
    return render_template('admin/add_course.html', title='Add Course', form=form)

@bp.route('/manage_students')
@login_required
def manage_students():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    
    students = Student.query.all()
    return render_template('admin/manage_students.html', 
                         title='Manage Students',
                         students=students)