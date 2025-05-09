from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.student import bp
from app.models import Student, Result, Notification

@bp.route('/notifications')
@login_required
def notifications():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    student = current_user.student
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('main.index'))
    notifications = Notification.query.filter_by(user_id=student.user_id).order_by(Notification.created_at.desc()).all()
    return render_template('student/notifications.html', notifications=notifications)


@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('main.index'))
    
    # Get latest results
    latest_results = Result.query.filter_by(student_id=student.id)\
                                .order_by(Result.academic_year.desc(), Result.semester.desc())\
                                .limit(5).all()

    # Get current level and recent semester (if possible)
    current_level = student.level
    # Try to get the most recent semester for this level
    recent_result = Result.query.filter_by(student_id=student.id, academic_year=current_level)\
                                .order_by(Result.semester.desc()).first()
    current_semester = recent_result.semester if recent_result else None

    # Calculate GPA for current semester (if available)
    semester_gpa = student.calculate_gpa_for_semester(current_semester, current_level) if current_semester else None
    # Calculate CGPA for current level
    level_cgpa = student.calculate_cgpa_for_year(current_level)
    # Calculate true university-wide CGPA
    overall_cgpa = student.calculate_overall_cgpa()

    return render_template('student/dashboard.html',
                         title='Student Dashboard',
                         student=student,
                         results=latest_results,
                         semester_gpa=semester_gpa,
                         level_cgpa=level_cgpa,
                         overall_cgpa=overall_cgpa)

@bp.route('/results')
@login_required
def view_results():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('main.index'))
    
    # Group results by academic year and semester
    results = Result.query.filter_by(student_id=student.id)\
                         .order_by(Result.academic_year.desc(), Result.semester.desc())\
                         .all()
    
    # Organize results by semester
    semester_results = {}
    for result in results:
        key = f"{result.academic_year} - {result.semester}"
        if key not in semester_results:
            semester_results[key] = {
                'results': [],
                'gpa': student.calculate_gpa(result.semester, result.academic_year)
            }
        semester_results[key]['results'].append(result)
    
    return render_template('student/results.html',
                         title='My Results',
                         semester_results=semester_results)