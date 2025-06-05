import os
from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash
import jwt
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from app.models import User, Student, AuditLog
from app.utils.email import send_password_reset_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Strip whitespace from input
        user_input = form.username.data.strip()
        password_input = form.password.data
        user = User.query.filter((User.username == user_input) | (User.email == user_input)).first()
        if user is None:
            flash('No user found with that username or email.', 'danger')
            return redirect(url_for('auth.login'))
        print('DEBUG: Stored hash:', user.password_hash)
        print('DEBUG: Password entered:', password_input)
        print('DEBUG: Password check result:', user.check_password(password_input))
        if not user.check_password(password_input):
            flash('Password is incorrect for this account.', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        # Log login event
        from app.models import LoginHistory
        login_record = LoginHistory(user_id=user.id, ip_address=request.remote_addr)
        db.session.add(login_record)
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            # Redirect students to their dashboard
            if user.is_admin():
                next_page = url_for('admin.dashboard')
            else:
                next_page = url_for('student.dashboard')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check for duplicate username or email
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return render_template('auth/register.html', title='Register', form=form)

        # Check for duplicate index number
        existing_student = Student.query.filter_by(index_number=form.index_number.data).first()
        if existing_student:
            flash('Index number already exists. Please check your details or contact admin.', 'danger')
            return render_template('auth/register.html', title='Register', form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            user_type='student'
        )
        user.set_password(form.password.data)
        print('DEBUG REGISTRATION: Password entered:', form.password.data)
        print('DEBUG REGISTRATION: Generated hash:', user.password_hash)
        db.session.add(user)
        db.session.flush()  # Assigns user.id for the foreign key

        student = Student(
            user=user,
            index_number=form.index_number.data,
            full_name=form.full_name.data,
            program=form.program.data,
            level=form.level.data
        )
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered student!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def get_reset_token(user, expires_sec=3600):
    """Generate a JWT token for password reset."""
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_sec)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def verify_reset_token(token):
    """Verify the password reset token and return the user if valid."""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload.get('user_id')
        return User.query.get(user_id)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            try:
                send_password_reset_email(user)
                flash('An email has been sent with instructions to reset your password.', 'info')
                return redirect(url_for('auth.login'))
            except Exception as e:
                current_app.logger.error(f'Error sending password reset email: {str(e)}')
                flash('An error occurred while sending the password reset email. Please try again later.', 'danger')
        else:
            # Don't reveal that the email doesn't exist for security reasons
            flash('If an account exists with this email, you will receive a password reset link.', 'info')
            return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    user = verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_password_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Update the user's password
        user.password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        db.session.commit()
        
        # Log the password reset
        log = AuditLog(
            admin_id=user.id,  # self-initiated
            action='Password Reset',
            target_type='User',
            target_id=user.id,
            details='User reset their password via email'
        )
        db.session.add(log)
        db.session.commit()
        
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', title='Reset Password', form=form)