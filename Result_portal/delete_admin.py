import pymysql
from dotenv import load_dotenv
import os

def delete_admin():
    # Load environment variables
    load_dotenv()
    
    # Parse database URL from environment
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in .env file")
        return False
    
    # Extract database connection details
    # Format: mysql+pymysql://username:password@host:port/database
    parts = db_url.split('//')[1].split('@')
    user_pass = parts[0].split(':')
    db_user = user_pass[0]
    db_pass = user_pass[1]
    
    host_db = parts[1].split('/')
    db_host = host_db[0].split(':')[0] if ':' in host_db[0] else host_db[0]
    db_name = host_db[1].split('?')[0]  # Remove any query parameters
    
    # Database connection parameters
    db_config = {
        'host': db_host,
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
            # Delete admin user
            sql = "DELETE FROM `users` WHERE `username` = 'admin'"
            cursor.execute(sql)
            connection.commit()
            
            if cursor.rowcount > 0:
                print("Admin user deleted successfully!")
                return True
            else:
                print("No admin user found to delete.")
                return False
                
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
    
    delete_admin()
