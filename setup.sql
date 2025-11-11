--database detup script for Student Management System
--script creates database, table, and populates initial data

--create database students_db;

--\c students_db

--drop table if exists (for clean setup)
DROP TABLE IF EXISTS students;

--create students table with specified schema
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,        --auto-incrementing primary key
    first_name TEXT NOT NULL,              --student's first name (required)
    last_name TEXT NOT NULL,               --student's last name (required)
    email TEXT NOT NULL UNIQUE,            --student's email (required and unique)
    enrollment_date DATE                   --date of enrollment
);

--insert initial data
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');

--verify the data was inserted correctly
SELECT * FROM students;