from app import create_app, db
from app.models import Student, Program, Level, User

def list_students():
    app = create_app()
    
    with app.app_context():
        # Get all students with their related data
        students = Student.query.join(User, Student.user_id == User.id)\
                              .join(Program, Student.program_id == Program.id)\
                              .join(Level, Student.level_id == Level.id)\
                              .with_entities(
                                  Student.id,
                                  Student.index_number,
                                  Student.full_name,
                                  Program.name.label('program_name'),
                                  Level.name.label('level_name'),
                                  User.email,
                                  Student.archived
                              )\
                              .order_by(Student.index_number)\
                              .all()
        
        if not students:
            print("No students found in the database.")
            return
        
        # Print header
        print("\n{:<5} {:<15} {:<30} {:<30} {:<15} {:<30} {:<10}".format(
            "ID", "Index Number", "Full Name", "Program", "Level", "Email", "Archived"
        ))
        print("-" * 120)
        
        # Print each student's details
        for student in students:
            print("{:<5} {:<15} {:<30} {:<30} {:<15} {:<30} {:<10}".format(
                student.id,
                student.index_number,
                student.full_name[:28] + '...' if len(student.full_name) > 28 else student.full_name,
                student.program_name[:28] + '...' if len(student.program_name) > 28 else student.program_name,
                student.level_name,
                student.email,
                'Yes' if student.archived else 'No'
            ))
        
        # Print summary
        print("\nTotal students:", len(students))
        print("Active students:", sum(1 for s in students if not s.archived))
        print("Archived students:", sum(1 for s in students if s.archived))

def list_programs():
    app = create_app()
    
    with app.app_context():
        programs = Program.query.order_by(Program.name).all()
        
        if not programs:
            print("No programs found in the database.")
            return
        
        print("\nAvailable Programs:")
        print("ID  Name")
        print("-" * 50)
        for program in programs:
            print(f"{program.id:<3} {program.name}")

def list_levels():
    app = create_app()
    
    with app.app_context():
        levels = Level.query.order_by(Level.name).all()
        
        if not levels:
            print("No levels found in the database.")
            return
        
        print("\nAvailable Levels:")
        print("ID  Name")
        print("-" * 50)
        for level in levels:
            print(f"{level.id:<3} {level.name}")

if __name__ == '__main__':
    print("Fetching student details...")
    list_levels()
    list_programs()
    list_students()
