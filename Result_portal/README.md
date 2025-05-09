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

This guide will help you set up and use the Student Result Portal, even if you close everything and want to start again later. Each step is explained for clarity.

---

### 1. Clone the Repository
Download the project code from your repository:
```bash
git clone <your-repo-url>
cd student_result_portal
```

### 2. Create and Activate a Virtual Environment
A virtual environment keeps your dependencies organized.
```bash
python -m venv venv
```
- **On Windows CMD:**
  ```cmd
  venv\Scripts\activate
  ```
- **On Windows PowerShell:**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
You should see `(venv)` at the start of your prompt.

---

### 3. Install Dependencies
Install all required Python packages:
```bash
pip install -r requirements.txt
```
If you get errors about missing packages, install them manually:
```bash
pip install flask flask_sqlalchemy flask_migrate flask_login flask_bootstrap flask_wtf python-dotenv pymysql cryptography
```

---

### 4. Set Up Environment Variables
Environment variables store your secrets and DB info.
- Copy `.env.example` to `.env` and edit with your credentials:
  ```bash
  cp .env.example .env
  ```
- Or create a `.env` file with:
  ```
  SECRET_KEY=your-secret-key-here
  DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/student_result_portal
  ```
  Replace with your actual MySQL username, password, and database name.

---

### 5. Set the Flask App Environment Variable
This tells Flask how to find your app.
- **On Windows CMD:**
  ```cmd
  set FLASK_APP=app:create_app
  ```
- **On PowerShell:**
  ```powershell
  $env:FLASK_APP = "app:create_app"
  ```
- **On macOS/Linux:**
  ```bash
  export FLASK_APP=app:create_app
  ```

---

### 6. Initialize the Database (First Time Only)
Set up the database tables:
```bash
python -m flask db init
python -m flask db migrate
python -m flask db upgrade
```
#### If you add new fields to models (e.g., 'archived' to Student):
If you add a new field and are **not** using Flask-Migrate, run this SQL in your MySQL client:
```sql
ALTER TABLE students ADD COLUMN archived BOOLEAN NOT NULL DEFAULT 0;
```

---

### 7. How to Start the App (Anytime)
If you close everything and want to start again:
1. Open your terminal and go to your project folder:
   ```bash
   cd student_result_portal
   ```
2. Activate your virtual environment:
   - Windows CMD: `venv\Scripts\activate`
   - PowerShell: `.\venv\Scripts\Activate.ps1`
   - macOS/Linux: `source venv/bin/activate`
3. Set the Flask app environment variable (see Step 5).
4. Start the server:
   ```bash
   python run.py
   # or
   python -m flask run
   ```
5. Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

---

### 8. Accessing Routes
- Home: `/`
- Auth: `/auth/login`, `/auth/register`
- Admin: `/admin/dashboard`
- Student: `/student/dashboard`

---

### Troubleshooting
- If you get `flask is not recognized`, activate your virtual environment and use `python -m flask ...`.
- If you get `ModuleNotFoundError`, install the missing package with `pip install <package-name>` inside your virtual environment.
- If you get import errors related to blueprints or your app, double-check the `FLASK_APP` setting and your `__init__.py` files.

---

## Features
- Modular Flask blueprints for auth, admin, and student logic
- WTForms for secure form handling
- Environment variable management with `.env` files
- Professional folder structure for scalability
- Static files for CSS/JS
- Ready-to-use templates for all major pages

### Modern Admin Result Entry Workflow
- **Step-by-step Filtering:** Admins now enter results using a multi-step process:
  1. **Select Program**: Choose the student's program of study.
  2. **Select Level**: Choose the academic level (100, 200, 300, 400).
  3. **Select Student**: Only students in the chosen program and level are shown.
  4. **Select Course**: Courses are shown after a student is selected.
  5. **Enter Result Details**: Fill in score, semester, academic year, and remarks.
- **Modern Professional UI:** The form is responsive, visually clear, and disables fields until prerequisites are selected, preventing errors and confusion.
- **Scalable for Large Institutions:** The filtering workflow ensures admins can efficiently locate the right student and course, even in large datasets.

#### Usage Example (Admin Result Entry)
1. Go to the **Enter Result** page in the admin dashboard.
2. Select a Program. The Level dropdown is enabled.
3. Select a Level. The Student dropdown is enabled and only shows students in that program & level.
4. Select a Student. The Course dropdown is enabled.
5. Enter the result details and submit.

If no students or courses are available for the selected filters, the system will notify you.

## .env.example

A `.env.example` file is included for sharing the required environment variable structure. Copy it to `.env` and fill in your secrets.

## Forms and Templates

This project uses WTForms for form handling and includes templates for authentication, admin, and student modules. See the `forms.py` and `templates/` directories for examples and extend as needed.

---

For any issues, please check your environment variables, database connection, and installed dependencies.

For help with authentication, admin dashboard, or other features, open an issue or contact the maintainer.
