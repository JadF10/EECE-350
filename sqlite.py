import sqlite3

# Connect to SQLite (in memory for testing)
conn = sqlite3.connect(':memory:')

# this is important because foreign keys are OFF by default in SQLite
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# Helper function to inspect table contents
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))

# Create tables

cursor.execute("""
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")
cursor.execute("""
CREATE TABLE registered_courses (
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")
cursor.execute("""
CREATE TABLE grades (
    student_id INT,
    course_id INT,
    grade REAL,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")

students = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21)
]
cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)




registered = [
    (1, 101),
    (1, 102),
    (2, 101),
    (3, 103)
]
cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", registered)

grades = [
    (1, 101, 85),
    (1, 102, 92),
    (2, 101, 78),
    (3, 103, 88)
]
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades)
conn.commit()
print_table(cursor, "student")
print_table(cursor, "registered_courses")
print_table(cursor, "grades")

# --- Max and Average Grades per Student
# -------------------------

# FIX HERE: Your previous code only calculated for student_id = 1
# We loop over all students
for student_id in [1, 2, 3]:
    # Max grade
    cursor.execute("""
    SELECT MAX(grade), course_id
    FROM grades
    WHERE student_id = ?
    """, (student_id,))
    max_grade, course_id = cursor.fetchone()
    print(f"\nStudent {student_id} Maximum grade: {max_grade}, Course ID: {course_id}")

    # Average grade
    cursor.execute("""
    SELECT AVG(grade)
    FROM grades
    WHERE student_id = ?
    """, (student_id,))
    avg_grade = cursor.fetchone()[0]
    print(f"Student {student_id} Average grade: {avg_grade:.2f}")

# -------------------------
# Close Connection
# -------------------------
# FIX HERE: Close connection **after all operations**
conn.close()

