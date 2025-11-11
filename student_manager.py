import psycopg2
from psycopg2 import Error
from datetime import datetime

class StudentDatabase:
    """class to manage database connection and operations"""
    
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        """initialize database connection parameters"""
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """establish connection to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Successfully connected to PostgreSQL database")
            return True
        except Error as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            return False
    
    def disconnect(self):
        """close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Database connection closed")
    
    def getAllStudents(self):
        """retrieve and display all records from the students table"""
        try:
            query = "SELECT * FROM students ORDER BY student_id;"
            self.cursor.execute(query)
            students = self.cursor.fetchall()
            
            #display results in formatted table
            print("\n" + "="*80)
            print("ALL STUDENTS")
            print("="*80)
            print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Enrollment Date':<15}")
            print("-"*80)
            
            for student in students:
                print(f"{student[0]:<5} {student[1]:<15} {student[2]:<15} {student[3]:<30} {student[4]}")
            
            print(f"\nTotal students: {len(students)}")
            print("="*80 + "\n")
            
            return students
            
        except Error as e:
            print(f"Error retrieving students: {e}")
            return None
    
    def addStudent(self, first_name, last_name, email, enrollment_date):
        """insert a new student record into the students table"""
        try:
            query = """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
            """
            self.cursor.execute(query, (first_name, last_name, email, enrollment_date))
            student_id = self.cursor.fetchone()[0]
            self.connection.commit()
            
            print(f"\n✓ Successfully added student: {first_name} {last_name} (ID: {student_id})")
            return True
            
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error adding student: {e}")
            return False
    
    def updateStudentEmail(self, student_id, new_email):
        """update the email address for a student with the specified student_id"""
        try:
            #check to see if the student exists
            check_query = "SELECT first_name, last_name FROM students WHERE student_id = %s;"
            self.cursor.execute(check_query, (student_id,))
            student = self.cursor.fetchone()
            
            if not student:
                print(f"\n✗ Student with ID {student_id} not found")
                return False
            
            #update email
            update_query = "UPDATE students SET email = %s WHERE student_id = %s;"
            self.cursor.execute(update_query, (new_email, student_id))
            self.connection.commit()
            
            print(f"\n✓ Successfully updated email for {student[0]} {student[1]} (ID: {student_id})")
            print(f"  New email: {new_email}")
            return True
            
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error updating email: {e}")
            return False
    
    def deleteStudent(self, student_id):
        """delete the record of the student with the specified student_id"""
        try:
            #check to see if teh student exists
            check_query = "SELECT first_name, last_name FROM students WHERE student_id = %s;"
            self.cursor.execute(check_query, (student_id,))
            student = self.cursor.fetchone()
            
            if not student:
                print(f"\n✗ Student with ID {student_id} not found")
                return False
            
            #delete student
            delete_query = "DELETE FROM students WHERE student_id = %s;"
            self.cursor.execute(delete_query, (student_id,))
            self.connection.commit()
            
            print(f"\n✓ Successfully deleted student: {student[0]} {student[1]} (ID: {student_id})")
            return True
            
        except Error as e:
            self.connection.rollback()
            print(f"\n✗ Error deleting student: {e}")
            return False


def display_menu():
    """display the main menu options"""
    print("\n" + "="*50)
    print("STUDENT MANAGEMENT SYSTEM")
    print("="*50)
    print("1. View all students")
    print("2. Add new student")
    print("3. Update student email")
    print("4. Delete student")
    print("5. Exit")
    print("="*50)


def main():
    """main function to run the application"""
    print("Welcome to Student Management System")
    print("-" * 50)
    
    #database connection parameters
    dbname = "students_db"
    user = "postgres"
    password = "password" #my pgAdmin password, change to yours(TA) if needed
    host = "localhost"
    port = "5432"
    
    print(f"Connecting to database: {dbname}")
    print(f"Host: {host}:{port}")
    print(f"User: {user}\n")
    
    #create database instance and connect
    db = StudentDatabase(dbname, user, password, host, port)
    
    if not db.connect():
        print("Failed to connect to database. Exiting...")
        return
    
    #main application loop
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            #get all students
            db.getAllStudents()
            
        elif choice == '2':
            #add new student
            print("\n--- Add New Student ---")
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            email = input("Email: ").strip()
            enrollment_date = input("Enrollment date (YYYY-MM-DD): ").strip()
            
            db.addStudent(first_name, last_name, email, enrollment_date)
            
        elif choice == '3':
            #update student email
            print("\n--- Update Student Email ---")
            try:
                student_id = int(input("Student ID: ").strip())
                new_email = input("New email: ").strip()
                db.updateStudentEmail(student_id, new_email)
            except ValueError:
                print("Invalid student ID. Please enter a number.")
            
        elif choice == '4':
            #delete student
            print("\n--- Delete Student ---")
            try:
                student_id = int(input("Student ID: ").strip())
                confirm = input(f"Are you sure you want to delete student {student_id}? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    db.deleteStudent(student_id)
                else:
                    print("Delete operation cancelled.")
            except ValueError:
                print("Invalid student ID. Please enter a number.")
            
        elif choice == '5':
            print("\nThank you for using Student Management System!")
            break
            
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 5.")
        
        input("\nPress Enter to continue...")
    
    #disconnect from database
    db.disconnect()


if __name__ == "__main__":
    main()