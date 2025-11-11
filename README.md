COMP3005A - Assignment 3 - Q(1)
Mohamad Deifallah
101123377
2025-11-09


STUDENT MANAGEMENT SYSTEM

A Python application that connects to a PostgreSQL database to perform CRUD operations on student records.

Video Demonstration

https://youtu.be/UjJaWRuzf8w

SETUP INSTRUCTIONS

Prerequisites:

- PostgreSQL installed
- Python 3.x installed
- psycopg2 library

Database Setup:

1. Open pgAdmin
2. Create a new database called students_db
3. Open the Query Tool
4. Run the setup.sql script

Application Setup:

1. Clone the Repository:

git clone https://github.com/officialmd/COMP-3005---Student-Management-System
cd COMP-3005---Student_Management_System

2. Install required library:

pip install psycopg2-binary

3. Update database password in student_manager.py (line 184):

password = "password"

4. Run the application:

python student_manager.py

FUNCTIONS

getAllStudents()                                                - Retrieves and displays all student records from the database.

addStudent(first_name, last_name, email, enrollment_date)       - Adds a new student to the database.

updateStudentEmail(student_id, new_email)                       - Updates the email address for a specific student.

deleteStudent(student_id)                                       - Deletes a student record from the database.

USAGE

The application provides a menu with 5 options:
1. View all students
2. Add new student
3. Update student email
4. Delete student
5. Exit

Enter the number of your choice and follow the prompts.

DATABASE SCHEMA

Table: students
- student_id (SERIAL, PRIMARY KEY)
- first_name (TEXT, NOT NULL)
- last_name (TEXT, NOT NULL)
- email (TEXT, NOT NULL, UNIQUE)
- enrollment_date (DATE)
