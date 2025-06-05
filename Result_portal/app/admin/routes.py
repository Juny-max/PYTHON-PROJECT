from flask import render_template, flash, redirect, url_for, request, current_app, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import csv
from datetime import datetime
from flask import Blueprint
from app import db
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.admin.forms import UploadResultsForm, AddCourseForm, EditStudentForm, EnterResultForm, StudentSearchForm
from app.models import User, Student, Course, Result, Program, Level, AuditLog
from app.utils import allowed_file
from app.utils.email import send_welcome_email
#from app.models import ProgramCourse

# Create and configure the admin blueprint
bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    
    # Total students count (not archived)
    total_students = Student.query.filter_by(archived=0).count()

    # Programs and student counts
    program_counts = (
        db.session.query(Program, func.count(Student.id))
        .outerjoin(Student, (Student.program_id == Program.id) & (Student.archived == 0))
        .group_by(Program.id)
        .all()
    )

    # Recent results with related info
    recent_results = (
        db.session.query(Result)
        .join(Student, Result.student_id == Student.id)
        .join(Program, Student.program_id == Program.id)
        .join(Course, Result.course_id == Course.id)
        .order_by(Result.uploaded_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        program_counts=program_counts,
        recent_results=recent_results,
        student_count=total_students,  # if used elsewhere
        archived_count=Student.query.filter_by(archived=1).count(),
        program_count=Program.query.count(),
        course_count=Course.query.count()
    )

@bp.route('/audit_logs')
@login_required
def audit_logs():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import AuditLog
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template('admin/audit_logs.html', logs=logs)

    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    total_students = Student.query.count()
    total_courses = Course.query.count()
    
    # Get recent results with program names
    recent_results = Result.query.join(Student).join(Program).order_by(Result.uploaded_at.desc()).limit(5).all()
    
    # Get all programs and count of students per program (excluding archived)
    program_counts = db.session.query(
        Program.name, db.func.count(Student.id)
    ).join(Student, Program.id == Student.program_id).filter(Student.archived == False).group_by(Program.name).all()

    return render_template('admin/dashboard.html', 
                         title='Admin Dashboard',
                         total_students=total_students,
                         total_courses=total_courses,
                         recent_results=recent_results,
                         program_counts=program_counts)


@bp.route('/send_notification', methods=['GET', 'POST'])
@login_required
def send_notification():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.admin.forms import SendNotificationForm
    from app.models import Student, Notification
    form = SendNotificationForm()
    # Populate student choices
    students = Student.query.filter_by(archived=False).all()
    form.student.choices = [(s.id, f"{s.full_name} ({s.index_number})") for s in students]
    if form.validate_on_submit():
        student = Student.query.get(form.student.data)
        notif = Notification(user_id=student.user_id, message=form.message.data)
        db.session.add(notif)
        db.session.commit()
        # Log audit
        from app.models import AuditLog
        log = AuditLog(admin_id=current_user.id, action='Send Notification', target_type='Student', target_id=student.id, details=f'Sent notification to {student.full_name} ({student.index_number})')
        db.session.add(log)
        db.session.commit()
        flash('Notification sent!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/send_notification.html', form=form)

@bp.route('/broadcast_message', methods=['GET', 'POST'])
@login_required
def broadcast_message():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.admin.forms import BroadcastMessageForm
    from app.models import Student, Notification
    form = BroadcastMessageForm()
    if form.validate_on_submit():
        students = Student.query.filter_by(archived=False)
        if form.program.data:
            students = students.filter(Student.program.ilike(f"%{form.program.data}%"))
        if form.level.data and form.level.data != '':
            students = students.filter_by(level=form.level.data)
        students = students.all()
        for s in students:
            notif = Notification(user_id=s.user_id, message=form.message.data)
            db.session.add(notif)
        db.session.commit()
        # Log audit
        from app.models import AuditLog
        log = AuditLog(admin_id=current_user.id, action='Broadcast Notification', target_type='Student', target_id=None, details=f'Broadcasted notification to {len(students)} students')
        db.session.add(log)
        db.session.commit()
        flash(f'Broadcast sent to {len(students)} students!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/broadcast_message.html', form=form)

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

@bp.route('/manage_courses')
@login_required
def manage_courses():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    courses = Course.query.all()
    return render_template('admin/manage_courses.html', title='Manage Courses', courses=courses, show_programs=False)

@bp.route('/manage_programs', defaults={'program_id': None})
@bp.route('/manage_programs/<int:program_id>')
@login_required
def manage_programs(program_id=None):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program, Course, Student
    programs = Program.query.filter_by(archived=False).all()
    archived_programs = Program.query.filter_by(archived=True).all()
    all_courses = Course.query.all()
    selected_program = Program.query.get(program_id) if program_id else None
    # Find unique student programs not yet in Program table
    student_programs = set([s.program.name for s in Student.query.join(Program).distinct() if s.program])
    program_names = set([p.name for p in programs] + [p.name for p in archived_programs])
    missing_programs = sorted(list(student_programs - program_names))
    return render_template('admin/manage_courses.html', title='Manage Programs',
                           show_programs=True, programs=programs, archived_programs=archived_programs,
                           selected_program=selected_program, all_courses=all_courses,
                           missing_programs=missing_programs)

@bp.route('/import_student_program', methods=['POST'])
@login_required
def import_student_program():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program
    name = request.form.get('import_program_name')
    if name:
        program = Program(name=name)
        db.session.add(program)
        db.session.commit()
        flash(f'Imported program "{name}" from students.', 'success')
    else:
        flash('No program name provided.', 'danger')
    return redirect(url_for('admin.manage_programs'))

@bp.route('/edit_program/<int:program_id>', methods=['GET', 'POST'])
@login_required
def edit_program(program_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program
    program = Program.query.get_or_404(program_id)
    if request.method == 'POST':
        name = request.form.get('edit_program_name')
        description = request.form.get('edit_program_description')
        if name:
            program.name = name
            program.description = description
            db.session.commit()
            flash('Program updated successfully!', 'success')
            return redirect(url_for('admin.manage_programs', program_id=program_id))
        else:
            flash('Program name is required.', 'danger')
    return render_template('admin/edit_program.html', program=program)

@bp.route('/add_program', methods=['POST'])
@login_required
def add_program():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program
    name = request.form.get('name')
    description = request.form.get('description')
    if name:
        program = Program(name=name, description=description)
        db.session.add(program)
        db.session.commit()
        flash('Program added successfully!', 'success')
    else:
        flash('Program name is required.', 'danger')
    return redirect(url_for('admin.manage_programs'))

@bp.route('/delete_program/<int:program_id>', methods=['POST'])
@login_required
def delete_program(program_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program
    program = Program.query.get_or_404(program_id)
    db.session.delete(program)
    db.session.commit()
    flash('Program deleted successfully!', 'success')
    return redirect(url_for('admin.manage_programs'))

@bp.route('/archive_program/<int:program_id>', methods=['POST'])
@login_required
def archive_program(program_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program
    program = Program.query.get_or_404(program_id)
    program.archived = True
    db.session.commit()
    flash('Program archived successfully!', 'success')
    return redirect(url_for('admin.manage_programs'))

@bp.route('/restore_program/<int:program_id>', methods=['POST'])
@login_required
def restore_program(program_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program
    program = Program.query.get_or_404(program_id)
    program.archived = False
    db.session.commit()
    flash('Program restored successfully!', 'success')
    return redirect(url_for('admin.manage_programs'))

@bp.route('/add_course_to_program/<int:program_id>', methods=['POST'])
@login_required
def add_course_to_program(program_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program, Course
    program = Program.query.get_or_404(program_id)
    course_id = request.form.get('course_id')
    course = Course.query.get(course_id)
    if course and course not in program.courses:
        program.courses.append(course)
        db.session.commit()
        flash('Course added to program.', 'success')
    else:
        flash('Invalid course selection or course already assigned.', 'danger')
    return redirect(url_for('admin.manage_programs', program_id=program_id))

@bp.route('/remove_course_from_program/<int:program_id>/<int:course_id>', methods=['POST'])
@login_required
def remove_course_from_program(program_id, course_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program, Course
    program = Program.query.get_or_404(program_id)
    course = Course.query.get_or_404(course_id)
    if course in program.courses:
        program.courses.remove(course)
        db.session.commit()
        flash('Course removed from program.', 'success')
    else:
        flash('Course not assigned to program.', 'danger')
    return redirect(url_for('admin.manage_programs', program_id=program_id))

@bp.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    course = Course.query.get_or_404(course_id)
    form = AddCourseForm(obj=course)
    if form.validate_on_submit():
        course.code = form.course_code.data
        course.title = form.course_title.data
        course.credit_hours = form.credit_hours.data
        db.session.commit()
        # Log audit
        from app.models import AuditLog
        log = AuditLog(admin_id=current_user.id, action='Edit Course', target_type='Course', target_id=course.id, details=f'Edited course {course.title} ({course.code})')
        db.session.add(log)
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin.manage_courses'))
    form.course_code.data = course.code
    form.course_title.data = course.title
    form.credit_hours.data = course.credit_hours
    return render_template('admin/add_course.html', title='Edit Course', form=form)

@bp.route('/delete_course/<int:course_id>')
@login_required
def delete_course(course_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    # Log audit
    from app.models import AuditLog
    log = AuditLog(admin_id=current_user.id, action='Delete Course', target_type='Course', target_id=course.id, details=f'Deleted course {course.title} ({course.code})')
    db.session.add(log)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('admin.manage_courses'))

@bp.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.models import Program, Course, AuditLog
    programs = Program.query.filter_by(archived=False).all()
    form = AddCourseForm()
    if request.method == 'POST':
        program_id = request.form.get('program_id')
        if not program_id or program_id == '':
            flash('You must select a program before adding a course.', 'danger')
            return render_template('admin/add_course.html', title='Add Course', form=form, programs=programs, selected_program_id=program_id)
        course = Course(
            code=form.course_code.data,
            title=form.course_title.data,
            credit_hours=form.credit_hours.data
        )
        db.session.add(course)
        db.session.commit()
        # Assign course to program
        program = Program.query.get(int(program_id))
        if program:
            program.courses.append(course)
            db.session.commit()
        # Log audit
        log = AuditLog(admin_id=current_user.id, action='Add Course', target_type='Course', target_id=course.id, details=f'Added course {course.title} ({course.code}) to program {program.name if program else "Unknown"}')
        db.session.add(log)
        db.session.commit()
        flash('Course added successfully!', 'success')
        return redirect(url_for('admin.manage_courses'))
    return render_template('admin/add_course.html', title='Add Course', form=form, programs=programs, selected_program_id=None)

@bp.route('/enter_result', methods=['GET', 'POST'])
@login_required
def enter_result():
    form = EnterResultForm()

    # Populate program and level choices
    programs = Program.query.filter_by(archived=False).all()
    levels = Level.query.filter_by(archived=False).all()
    form.program.choices = [(p.id, p.name) for p in programs]
    form.level.choices = [(l.id, l.name) for l in levels]

    selected_program = request.form.get('program', type=int)
    selected_level = request.form.get('level', type=int)

    # Populate students based on selected program and level
    if selected_program and selected_level:
        students = Student.query.filter_by(
            program_id=selected_program,
            level_id=selected_level,
            archived=False
        ).all()
        form.student.choices = [(s.id, f"{s.full_name} ({s.index_number})") for s in students]
    else:
        form.student.choices = []

    # Populate courses based on selected program
    if selected_program:
        program = Program.query.get(selected_program)
        courses = program.courses if program else []
        form.course.choices = [(c.id, f"{c.code} - {c.title}") for c in courses]
    else:
        form.course.choices = []

    # Handle form submission
    if form.validate_on_submit():
        student_id = form.student.data
        course_id = form.course.data
        score = form.score.data
        semester = form.semester.data
        academic_year = form.academic_year.data
        remarks = form.remarks.data

        # Check if result exists for this student, course, semester, and academic year
        existing_result = Result.query.filter_by(
            student_id=student_id,
            course_id=course_id,
            semester=semester,
            academic_year=academic_year
        ).first()

        grade = calculate_grade(score)

        if existing_result:
            # Update existing result
            existing_result.score = score
            existing_result.grade = grade
            existing_result.remarks = remarks
        else:
            # Create new result
            new_result = Result(
                student_id=student_id,
                course_id=course_id,
                score=score,
                grade=grade,
                semester=semester,
                academic_year=academic_year,
                remarks=remarks,
                uploaded_by=current_user.id
            )
            db.session.add(new_result)

        db.session.commit()
        flash('Result submitted successfully!', 'success')
        return redirect(url_for('admin.enter_result'))

    # Pass program name for readonly display in template
    program_name = ''
    if selected_program:
        program_obj = Program.query.get(selected_program)
        program_name = program_obj.name if program_obj else ''

    return render_template(
        'admin/enter_result.html',
        form=form,
        program=program_name,
        selected_program=selected_program,
        selected_level=selected_level,
    )

def calculate_grade(score):
    if score >= 80:
        return 'A'
    elif score >= 70:
        return 'A-'
    elif score >= 65:
        return 'B+'
    elif score >= 60:
        return 'B'
    elif score >= 55:
        return 'C+'
    elif score >= 50:
        return 'C'
    elif score >= 45:
        return 'D'
    elif score >= 40:
        return 'E'
    else:
        return 'F'

    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    results = Result.query.order_by(Result.uploaded_at.desc()).all()
    return render_template('admin/view_results.html', results=results)



@bp.route('/edit_result/<int:result_id>', methods=['GET', 'POST'])
@login_required
def edit_result(result_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    result = Result.query.get_or_404(result_id)
    from app.admin.forms import EnterResultForm
    form = EnterResultForm(obj=result)
    if form.validate_on_submit():
        student = Student.query.filter_by(index_number=form.index_number.data).first()
        course = Course.query.filter_by(code=form.course_code.data).first()
        if not student or not course:
            flash('Student or Course not found', 'danger')
            return render_template('admin/enter_result.html', form=form)
        result.student_id = student.id
        result.course_id = course.id
        result.score = form.score.data
        result.semester = form.semester.data
        result.academic_year = form.academic_year.data
        result.remarks = form.remarks.data
        result.grade = result.determine_grade()
        db.session.commit()
        # Log audit
        from app.models import AuditLog
        log = AuditLog(admin_id=current_user.id, action='Edit Result', target_type='Result', target_id=result.id, details=f'Edited result for student {result.student.index_number}, course {result.course.code}')
        db.session.add(log)
        db.session.commit()
        flash('Result updated successfully!', 'success')
        return redirect(url_for('admin.view_results'))
    # Prefill form fields
    form.index_number.data = result.student.index_number
    form.course_code.data = result.course.code
    form.score.data = result.score
    form.semester.data = result.semester
    form.academic_year.data = result.academic_year
    form.remarks.data = result.remarks
    from app.models import Program
    return render_template(
    'admin/enter_result.html',
    form=form,
    editing=True,
    programs=Program.query.filter_by(archived=False).all(),
    levels=['100', '200', '300', '400'],
    selected_program='',  # You can set this to the correct program id if available
    selected_level=result.student.level if hasattr(result.student, 'level') else '',
    program=result.student.program if hasattr(result.student, 'program') else '',
    courses=[(result.course.code, f"{result.course.code} - {result.course.title}")] if result.course else [],
)

@bp.route('/view_results', methods=['GET', 'POST'])
@login_required
def view_results():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    # Get filter options
    from app.models import Program
    programs = Program.query.filter_by(archived=False).all()
    levels = ['100', '200', '300', '400']

    # Get filter values from request
    selected_program = request.args.get('program', '')
    selected_level = request.args.get('level', '')

    # Query students based on filters
    students_query = Student.query.filter_by(archived=False)
    if selected_program:
        if selected_program != '':  # '' means 'All'
            students_query = students_query.join(Program).filter(Program.name == selected_program)
    if selected_level:
        students_query = students_query.filter(Student.level == selected_level)
    students = students_query.all()

    # Gather results for these students
    student_ids = [s.id for s in students]
    results = Result.query.filter(Result.student_id.in_(student_ids)).order_by(Result.academic_year.desc(), Result.semester.desc()).all()

    return render_template('admin/view_results.html',
        programs=programs,
        levels=levels,
        selected_program=selected_program,
        selected_level=selected_level,
        students=students,
        results=results)

@bp.route('/reports')
@login_required
def reports():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    total_students = Student.query.count()
    total_courses = Course.query.count()
    total_results = Result.query.count()
    pass_count = Result.query.filter(Result.grade.in_(['A', 'B', 'C', 'D'])).count()
    fail_count = Result.query.filter(Result.grade=='F').count()
    pass_rate = round((pass_count / total_results) * 100, 2) if total_results else 0
    fail_rate = round((fail_count / total_results) * 100, 2) if total_results else 0
    grades = ['A', 'B', 'C', 'D', 'F']
    grade_dist = {g: Result.query.filter(Result.grade==g).count() for g in grades}
    return render_template('admin/reports.html',
        total_students=total_students,
        total_courses=total_courses,
        total_results=total_results,
        pass_rate=pass_rate,
        fail_rate=fail_rate,
        grade_dist=grade_dist,
        now=datetime.now()
    )

@bp.route('/manage_students', methods=['GET', 'POST'])
@login_required
def manage_students():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    
    from app.admin.forms import ManageStudentForm
    form = ManageStudentForm()
    query = Student.query.options(  # Use a query object
        joinedload(Student.level),
        joinedload(Student.program)
    ).filter_by(archived=False)
    if form.validate_on_submit():
        if form.index_number.data:
            query = query.filter(Student.index_number.ilike(f"%{form.index_number.data}%"))
        if form.full_name.data:
            query = query.filter(Student.full_name.ilike(f"%{form.full_name.data}%"))
        if form.program.data:
            query = query.filter(Student.program.ilike(f"%{form.program.data}%"))
        if form.level.data and form.level.data != '':
            query = query.filter_by(level=form.level.data)
        if form.status.data == 'active':
            query = query.filter_by(archived=False)
        elif form.status.data == 'archived':
            query = query.filter_by(archived=True)
    students = query.all()  # Apply .all() only once, after all filters
    if not students:
        flash('No students found for the selected criteria.', 'warning')
    return render_template('admin/manage_students.html', 
                         title='Manage Students',
                         students=students,
                         form=form)

@bp.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
        
    from app.admin.forms import AddEditStudentForm
    from app.models import User, AuditLog
    from werkzeug.security import generate_password_hash
    from sqlalchemy.exc import IntegrityError
    
    form = AddEditStudentForm()
    
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.index_number.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            if existing_user.username == form.index_number.data:
                flash(f'Username {form.index_number.data} is already taken!', 'danger')
            if existing_user.email == form.email.data:
                flash(f'Email {form.email.data} is already registered!', 'danger')
            return render_template('admin/add_edit_student.html', form=form, editing=False)
        
        try:
            # Generate a random password if none provided
            password = form.password.data
            if not password or password.strip() == '':
                import random
                import string
                # Generate an 8-character password with letters, digits, and special characters
                characters = string.ascii_letters + string.digits + '!@#$%^&*'
                password = ''.join(random.choice(characters) for _ in range(8))
            
            # Create user with the generated or provided password
            user = User(
                username=form.index_number.data,
                email=form.email.data,
                user_type='student',
                password_hash=generate_password_hash(password, method='pbkdf2:sha256')
            )
            db.session.add(user)
            db.session.flush()  # Get user.id before commit
            
            # Get the program object
            program = Program.query.get(form.program.data)
            if not program:
                db.session.rollback()
                flash('Selected program not found', 'error')
                return redirect(url_for('admin.add_student'))
            
            # Get or create the level
            level_name = form.level.data
            level = Level.query.filter_by(name=level_name).first()
            if not level:
                # Create the level if it doesn't exist
                level = Level(name=level_name, description=f'Level {level_name}')
                db.session.add(level)
                db.session.flush()  # Get the level ID
            
            # Create student record
            student = Student(
                user_id=user.id,
                index_number=form.index_number.data,
                full_name=form.full_name.data,
                program_id=program.id,
                level_id=level.id,
                archived=False
            )
            db.session.add(student)
            
            # Log audit
            log = AuditLog(
                admin_id=current_user.id,
                action='Add Student',
                target_type='Student',
                target_id=student.id,
                details=f'Added student {student.full_name} ({student.index_number})'
            )
            db.session.add(log)
            
            db.session.commit()
            
            # Send welcome email with login credentials
            try:
                send_welcome_email(user, form.password.data)
                log.details += ' and sent welcome email'
                db.session.commit()
                flash('Student added successfully and welcome email sent!', 'success')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'Failed to send welcome email: {str(e)}')
                log.details += ' (email sending failed)'
                db.session.commit()
                flash('Student added but failed to send welcome email. Please notify the student manually.', 'warning')
            
            return redirect(url_for('admin.manage_students'))
            
        except IntegrityError as e:
            db.session.rollback()
            if 'duplicate entry' in str(e).lower() and 'username' in str(e).lower():
                flash(f'Username {form.index_number.data} is already taken!', 'danger')
            elif 'duplicate entry' in str(e).lower() and 'email' in str(e).lower():
                flash(f'Email {form.email.data} is already registered!', 'danger')
            else:
                current_app.logger.error(f'Error adding student: {str(e)}')
                flash('An error occurred while adding the student. Please try again.', 'danger')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Unexpected error adding student: {str(e)}')
            flash('An unexpected error occurred. Please try again.', 'danger')
    
    return render_template('admin/add_edit_student.html', form=form, editing=False)

@bp.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    
    student = Student.query.get_or_404(student_id)
    form = EditStudentForm()
    
    if form.validate_on_submit():
        try:
            student.full_name = form.full_name.data
            
            # Find the program by name and update the program_id
            program = Program.query.filter_by(name=form.program.data).first()
            if program:
                student.program_id = program.id
            else:
                flash('Program not found!', 'error')
                return redirect(url_for('admin.edit_student', student_id=student_id))
            
            # Find the level by name and update the level_id
            level = Level.query.filter_by(name=form.level.data).first()
            if level:
                student.level_id = level.id
            else:
                flash('Level not found!', 'error')
                return redirect(url_for('admin.edit_student', student_id=student_id))
            
            db.session.commit()
            
            # Log audit
            log = AuditLog(
                admin_id=current_user.id,
                action='Edit Student',
                target_type='Student',
                target_id=student.id,
                details=f'Edited student {student.full_name} ({student.index_number})'
            )
            db.session.add(log)
            db.session.commit()
            
            flash('Student updated successfully!', 'success')
            return redirect(url_for('admin.manage_students'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'error')
            return redirect(url_for('admin.edit_student', student_id=student_id))
    
    # If GET request or validation failed, pre-populate the form
    form.full_name.data = student.full_name
    if student.program_id:
        program = Program.query.get(student.program_id)
        if program:
            form.program.data = program.name
    if student.level_id:
        level = Level.query.get(student.level_id)
        if level:
            form.level.data = level.name
    
    return render_template('admin/edit_student.html', form=form, student=student, no_program=not student.program_id)
@bp.route('/archive_student/<int:student_id>')
@login_required
def archive_student(student_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    student = Student.query.get_or_404(student_id)
    student.archived = True
    db.session.commit()
    # Log audit
    from app.models import AuditLog
    log = AuditLog(admin_id=current_user.id, action='Archive Student', target_type='Student', target_id=student.id, details=f'Archived student {student.full_name} ({student.index_number})')
    db.session.add(log)
    db.session.commit()
    flash('Student archived successfully!', 'success')
    return redirect(url_for('admin.manage_students'))

@bp.route('/export_students')
@login_required
def export_students():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    students = Student.query.filter_by(archived=False).all()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Index Number', 'Full Name', 'Program', 'Level'])
    for s in students:
        cw.writerow([s.index_number, s.full_name, s.program, s.level])
    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='students.csv')

@bp.route('/import_students', methods=['POST'])
@login_required
def import_students():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
        
    if 'file' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('admin.manage_students'))
        
    file = request.files['file']
    if not file or file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('admin.manage_students'))
        
    if not file.filename.lower().endswith('.csv'):
        flash('Only CSV files are allowed', 'danger')
        return redirect(url_for('admin.manage_students'))
    
    try:
        import io
        import csv
        import secrets
        import string
        from werkzeug.security import generate_password_hash
        from sqlalchemy.exc import IntegrityError
        from app.models import User, Student, Program, Level, AuditLog
        from app.utils.email import send_welcome_email
        
        # Read and parse the CSV file
        stream = io.StringIO(file.stream.read().decode('utf-8-sig'))  # Handle BOM if present
        reader = csv.DictReader(stream)
        
        # Initialize counters
        new_students = 0
        existing_students = 0
        email_errors = 0
        skipped_rows = []
        
        # Required fields
        required_fields = ['Index Number', 'Full Name', 'Program', 'Level']
        
        # Process each row in the CSV
        for row_num, row in enumerate(reader, start=2):  # Start at 2 for 1-based row numbers
            try:
                # Check for required fields
                if not all(row.get(field) for field in required_fields):
                    skipped_rows.append(f"Row {row_num}: Missing required fields")
                    continue
                    
                index_number = row['Index Number'].strip()
                full_name = row['Full Name'].strip()
                program_name = row['Program'].strip()
                level_name = row['Level'].strip()
                email = row.get('Email', '').strip() or f"{index_number}@student.portal"
                
                # Check if user already exists by username or email
                existing_user = User.query.filter(
                    (User.username == index_number) | 
                    (User.email == email)
                ).first()
                
                if existing_user:
                    existing_students += 1
                    continue
                
                # Start a transaction for this student
                try:
                    # Generate a secure random password
                    alphabet = string.ascii_letters + string.digits + '!@#$%^&*'
                    while True:
                        password = ''.join(secrets.choice(alphabet) for _ in range(12))
                        # Ensure password meets complexity requirements
                        if (any(c.islower() for c in password) and 
                            any(c.isupper() for c in password) and 
                            any(c.isdigit() for c in password)):
                            break
                    
                    # Create user
                    user = User(
                        username=index_number,
                        email=email,
                        user_type='student',
                        password_hash=generate_password_hash(password, method='pbkdf2:sha256')
                    )
                    db.session.add(user)
                    db.session.flush()
                    
                    # Get or create Program
                    program = Program.query.filter(
                        func.lower(Program.name) == func.lower(program_name)
                    ).first()
                    
                    if not program:
                        program = Program(
                            name=program_name,
                            description=f"Auto-created during student import on {datetime.utcnow().date()}",
                            archived=False
                        )
                        db.session.add(program)
                        db.session.flush()
                    
                    # Get or create Level
                    level = Level.query.filter(
                        func.lower(Level.name) == func.lower(level_name)
                    ).first()
                    
                    if not level:
                        level = Level(
                            name=level_name,
                            description=f"Level {level_name}",
                            archived=False
                        )
                        db.session.add(level)
                        db.session.flush()
                    
                    # Create student record
                    student = Student(
                        user_id=user.id,
                        index_number=index_number,
                        full_name=full_name,
                        program_id=program.id,
                        level_id=level.id,
                        archived=False
                    )
                    db.session.add(student)
                    
                    # Log the import
                    log = AuditLog(
                        admin_id=current_user.id,
                        action='Import Student',
                        target_type='Student',
                        target_id=student.id,
                        details=f'Imported student {full_name} ({index_number}) from CSV'
                    )
                    db.session.add(log)
                    
                    # Send welcome email
                    try:
                        send_welcome_email(user, password)
                        log.details += ' and sent welcome email'
                        new_students += 1
                    except Exception as e:
                        email_errors += 1
                        current_app.logger.error(f'Failed to send welcome email to {email}: {str(e)}')
                        log.details += ' (email sending failed)'
                    
                    # Commit the transaction for this student
                    db.session.commit()
                    
                except IntegrityError as e:
                    db.session.rollback()
                    if 'duplicate entry' in str(e).lower():
                        existing_students += 1
                    else:
                        current_app.logger.error(f'Error importing student {index_number}: {str(e)}')
                        skipped_rows.append(f"Row {row_num}: Database error - {str(e)}")
                
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'Error processing row {row_num}: {str(e)}')
                skipped_rows.append(f"Row {row_num}: {str(e)}")
        
        # Prepare flash message
        messages = []
        
        if new_students > 0:
            messages.append(f'Successfully imported {new_students} new students.')
            if email_errors > 0:
                messages.append(f'Failed to send {email_errors} welcome emails.')
        
        if existing_students > 0:
            messages.append(f'Skipped {existing_students} existing students (username or email already exists).')
        
        if skipped_rows:
            messages.append(f'Skipped {len(skipped_rows)} rows due to errors.')
            # Store detailed errors in session to display on a separate page if needed
            from flask import session
            session['import_errors'] = skipped_rows[-50:]  # Keep only the last 50 errors
        
        if not (new_students or existing_students or skipped_rows):
            messages.append('No valid student records found in the CSV file. Please check the file format.')
        
        # Join messages with line breaks
        flash('<br>'.join(messages), 'success' if new_students > 0 else 'warning')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error processing import: {str(e)}')
        flash(f'An error occurred while processing the file: {str(e)}', 'danger')
    
    return redirect(url_for('admin.manage_students'))

@bp.route('/bulk_students_action', methods=['POST'])
@login_required
def bulk_students_action():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    ids = request.form.getlist('student_ids')
    action = request.form.get('action')
    if not ids or not action:
        flash('No students selected or no action specified.', 'warning')
        return redirect(url_for('admin.manage_students'))
    students = Student.query.filter(Student.id.in_(ids)).all()
    if action == 'archive':
        for s in students:
            s.archived = True
        db.session.commit()
        flash(f'{len(students)} students archived.', 'success')
    elif action == 'delete':
        for s in students:
            db.session.delete(s)
        db.session.commit()
        flash(f'{len(students)} students deleted.', 'success')
    else:
        flash('Invalid action.', 'danger')
    return redirect(url_for('admin.manage_students'))

@bp.route('/archived_students')
@login_required
def archived_students():
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    students = Student.query.filter_by(archived=True).all()
    return render_template('admin/archived_students.html', students=students)

@bp.route('/reset_student_password/<int:student_id>', methods=['GET', 'POST'])
@login_required
def reset_student_password(student_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    from app.admin.forms import ResetStudentPasswordForm
    from app.models import User
    from werkzeug.security import generate_password_hash
    student = Student.query.get_or_404(student_id)
    user = User.query.get(student.user_id)
    form = ResetStudentPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        db.session.commit()
        # Log audit
        from app.models import AuditLog
        log = AuditLog(admin_id=current_user.id, action='Reset Password', target_type='Student', target_id=student.id, details=f'Reset password for {student.full_name} ({student.index_number})')
        db.session.add(log)
        db.session.commit()
        flash('Password reset successfully!', 'success')
        return redirect(url_for('admin.manage_students'))
    return render_template('admin/reset_student_password.html', form=form, student=student)

@bp.route('/view_login_history/<int:student_id>')
@login_required
def view_login_history(student_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    student = Student.query.get_or_404(student_id)
    from app.models import LoginHistory
    history = LoginHistory.query.filter_by(user_id=student.user_id).order_by(LoginHistory.timestamp.desc()).all()
    return render_template('admin/login_history.html', student=student, history=history)

@bp.route('/restore_student/<int:student_id>', methods=['POST'])
@login_required
def restore_student(student_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    student = Student.query.get_or_404(student_id)
    student.archived = False
    db.session.commit()
    flash('Student restored successfully.', 'success')
    return redirect(url_for('admin.archived_students'))

@bp.route('/delete_student/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    if not current_user.is_admin():
        return redirect(url_for('main.index'))
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    # Log audit
    from app.models import AuditLog
    log = AuditLog(admin_id=current_user.id, action='Delete Student', target_type='Student', target_id=student.id, details=f'Deleted student {student.full_name} ({student.index_number})')
    db.session.add(log)
    db.session.commit()
    flash('Student permanently deleted!', 'success')
    return redirect(url_for('admin.archived_students'))