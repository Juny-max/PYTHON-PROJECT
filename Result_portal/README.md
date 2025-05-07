# Student Result Portal

This project is a professional-grade web application for managing and viewing student results. It is built with Python, Flask, and MySQL (phpMyAdmin).

## Folder Structure

```
student_result_portal/
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── admin/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── student/
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   └── routes.py
│   ├── models.py
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── upload_results.html
│   │   │   └── manage_students.html
│   │   └── student/
│   │       ├── dashboard.html
│   │       └── results.html
│   └── utils.py
├── config.py
├── requirements.txt
├── .env.example
└── run.py
```

## Setup Instructions

### 1. Create a virtual environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Copy `.env.example` to `.env` and fill in your actual values:

```bash
cp .env.example .env
```

Or create a `.env` file with:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://username:password@localhost/student_result_portal
```

### 4. Initialize the database

```bash
flask db init
flask db migrate
flask db upgrade
```

### 5. Run the application

```bash
flask run
```

---

## Features
- Modular Flask blueprints for auth, admin, and student logic
- WTForms for secure form handling
- Environment variable management with `.env` files
- Professional folder structure for scalability
- Static files for CSS/JS
- Ready-to-use templates for all major pages

## .env.example

A `.env.example` file is included for sharing the required environment variable structure. Copy it to `.env` and fill in your secrets.

## Forms and Templates

This project uses WTForms for form handling and includes templates for authentication, admin, and student modules. See the `forms.py` and `templates/` directories for examples and extend as needed.

---

For any issues, please check your environment variables, database connection, and installed dependencies.

For help with authentication, admin dashboard, or other features, open an issue or contact the maintainer.
