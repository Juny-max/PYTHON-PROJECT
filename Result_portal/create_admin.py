import os
import sys
from werkzeug.security import generate_password_hash

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def create_admin_user():
    """
    Create an admin user with the following credentials:
    - Email: admin@portal.com
    - Password: admin123
    """
    app = create_app()
    
    with app.app_context():
        # Check if admin user already exists
        admin_email = 'admin@portal.com'
        existing_admin = User.query.filter_by(email=admin_email).first()
        
        if existing_admin:
            print(f"Admin user with email {admin_email} already exists.")
            print(f"User ID: {existing_admin.id}")
            return
        
        # Create new admin user
        admin = User(
            username='admin',
            email=admin_email,
            user_type='admin'
        )
        admin.set_password('admin123')  # This will hash the password
        
        try:
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created successfully with ID: {admin.id}")
            print(f"Email: {admin_email}")
            print("Password: admin123")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {str(e)}")

if __name__ == '__main__':
    create_admin_user()
