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
        return redirect(url_for('index'))
    notifications = Notification.query.filter_by(user_id=student.user_id).order_by(Notification.created_at.desc()).all()
    return render_template('student/notifications.html', notifications=notifications)


@bp.route('/dashboard')
@login_required
def dashboard():
    student = current_user.student
    
    # Get all results for the student
    results = Result.query.filter_by(student_id=student.id).all()
    
    # Calculate overall CGPA
    overall_cgpa = calculate_gpa(results)
    
    # Calculate current semester GPA
    current_semester_results = []
    current_semester_gpa = "N/A"
    
    if results:
        # Sort results by date and get the most recent semester
        sorted_results = sorted(results, key=lambda x: x.uploaded_at, reverse=True)
        if hasattr(sorted_results[0], 'semester'):
            current_semester = sorted_results[0].semester
            current_semester_results = [r for r in results if r.semester == current_semester]
        else:
            # If there's no semester attribute, group by academic year or another field
            # This is just an example - adjust based on your actual model
            current_semester_results = sorted_results[:5]  # Just use the 5 most recent results
        
        current_semester_gpa = calculate_gpa(current_semester_results)
    
    # For level CGPA, use a workaround since Result doesn't have level_id
    # Try to filter by student's current level
    level_results = results  # Default to all results
    level_cgpa = overall_cgpa  # Default to overall CGPA
    
    return render_template('student/dashboard.html',
                          title='Dashboard',
                          current_semester_gpa=current_semester_gpa,
                          level_cgpa=level_cgpa,
                          overall_cgpa=overall_cgpa,
                          results=results)

def calculate_gpa(results):
    if not results:
        return "N/A"
    
    # Define grade to grade point conversion based on your grading system
    def get_grade_point(grade=None, score=None):
        if grade:
            grade_to_point = {
                'A': 4.00,
                'A-': 3.85,
                'B+': 3.50,
                'B': 3.00,
                'C+': 2.50,
                'C': 2.00,
                'D': 1.50,
                'E': 1.00,
                'F': 0.00
            }
            return grade_to_point.get(grade, 0)
        elif score is not None:
            if score >= 80:
                return 4.00  # A
            elif score >= 70:
                return 3.85  # A-
            elif score >= 65:
                return 3.50  # B+
            elif score >= 60:
                return 3.00  # B
            elif score >= 55:
                return 2.50  # C+
            elif score >= 50:
                return 2.00  # C
            elif score >= 45:
                return 1.50  # D
            elif score >= 40:
                return 1.00  # E
            else:
                return 0.00  # F
        return 0.00
    
    total_credit_hours = 0
    total_quality_points = 0
    
    for r in results:
        # Get credit hours (make sure this attribute exists)
        credit_hours = getattr(r.course, 'credit_hours', 0)
        if credit_hours == 0:
            continue
            
        # Determine grade point based on either grade or score
        if hasattr(r, 'grade') and r.grade:
            grade_point = get_grade_point(grade=r.grade)
        elif hasattr(r, 'score'):
            grade_point = get_grade_point(score=r.score)
        else:
            continue  # Skip if neither grade nor score is available
        
        total_credit_hours += credit_hours
        total_quality_points += grade_point * credit_hours
    
    if total_credit_hours == 0:
        return "N/A"
    
    return round(total_quality_points / total_credit_hours, 2)

@bp.route('/results')
@login_required
def view_results():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    student = current_user.student
    if not student:
        flash('Student profile not found', 'danger')
        return redirect(url_for('index'))
    
    results = Result.query.filter_by(student_id=student.id).all()
    
    def year_to_level(year):
        mapping = {'1': '100', '2': '200', '3': '300', '4': '400'}
        return mapping.get(str(year), str(year))

    organized = {}
    semester_order = ['1', '2', 'First', 'Second']
    year_order = ['1', '2', '3', '4']

    for result in results:
        year = str(result.academic_year)
        semester = result.semester
        organized.setdefault(year, {})
        organized[year].setdefault(semester, []).append(result)

    display_results = []
    for year in sorted(organized.keys(), key=lambda x: (year_order.index(x) if x in year_order else 99, x)):
        level = year_to_level(year)
        year_group = {'year_code': year, 'level': level, 'semesters': []}
        for semester in sorted(organized[year].keys(), key=lambda x: (semester_order.index(x) if x in semester_order else x)):
            results_list = organized[year][semester]
            gpa = calculate_gpa(results_list)
            year_group['semesters'].append({
                'semester': semester,
                'results': results_list,
                'gpa': gpa
            })
        display_results.append(year_group)

    return render_template('student/results.html',
                           title='My Results',
                           display_results=display_results)