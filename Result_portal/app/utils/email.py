from flask import current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body=None, sync=False):
    """Send an email.
    
    Args:
        subject: Email subject
        sender: Sender email address
        recipients: List of recipient email addresses
        text_body: Plain text email body
        html_body: HTML email body (optional)
        sync: If True, send synchronously (default: False, sends asynchronously)
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
    
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

def send_welcome_email(user, password=None):
    """Send a welcome email to a new user.
    
    Args:
        user: User model instance
        password: Plain text password (only for new accounts)
    """
    subject = "Welcome to Student Result Portal"
    sender = current_app.config['MAIL_DEFAULT_SENDER']
    recipients = [user.email]
    
    # Render email templates
    text_body = render_template('email/welcome.txt', user=user, password=password)
    html_body = render_template('email/welcome.html', user=user, password=password)
    
    send_email(subject, sender, recipients, text_body, html_body)

def send_password_reset_email(user, token):
    """Send a password reset email.
    
    Args:
        user: User model instance
        token: Password reset token
    """
    subject = "Password Reset Request"
    sender = current_app.config['MAIL_DEFAULT_SENDER']
    recipients = [user.email]
    
    # Render email templates
    text_body = render_template('email/reset_password.txt', user=user, token=token)
    html_body = render_template('email/reset_password.html', user=user, token=token)
    
    send_email(subject, sender, recipients, text_body, html_body)
