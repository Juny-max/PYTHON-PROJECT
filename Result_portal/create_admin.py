import pymysql
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

def create_admin():
    # Load environment variables
    load_dotenv()
    
    # Parse database URL from environment
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        return False
        
    # Parse the database URL
    parsed = urlparse(db_url)
    
    # Extract components
    db_user = parsed.username
    db_pass = unquote(parsed.password)  # Decode URL-encoded password
    db_host = parsed.hostname
    db_port = parsed.port or 3306
    db_name = parsed.path.strip('/')
    
    # Database connection parameters
    db_config = {
        'host': db_host,
        'port': db_port,
        'user': db_user,
        'password': db_pass,
        'database': db_name,
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # Check if admin already exists
            sql = "SELECT * FROM `users` WHERE `username` = 'admin'"
            cursor.execute(sql)
            if cursor.fetchone():
                print("Admin user already exists!")
                return False
            
            # Create admin user
            password_hash = generate_password_hash('admin123', method='pbkdf2:sha256')
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            sql = """
                INSERT INTO `users` 
                (`username`, `email`, `password_hash`, `user_type`, `created_at`)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                'admin',
                'admin@example.com',
                password_hash,
                'admin',
                created_at
            ))
            
            connection.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("\nIMPORTANT: Please change this password after first login!")
            return True
            
    except pymysql.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

if __name__ == '__main__':
    # Install required package if not present
    try:
        import pymysql
    except ImportError:
        import sys
        import subprocess
        print("Installing required package: pymysql")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymysql"])
        import pymysql
    
    create_admin()
