import sqlite3

DB_NAME = "students.db"

SAMPLE_STUDENTS = [
    ("Sam", 20, "cse", 85),
    ("Rahul", 21, "ece", 78),
    ("Ankit", 19, "cse", 92),
    ("Priya", 20, "mech", 74),
    ("Neha", 22, "cse", 88),
    ("Rohan", 21, "mech", 66),
    ("Sneha", 19, "ece", 91),
    ("Aditya", 22, "ece", 59),
    ("Kavya", 20, "cse", 71),
    ("Arjun", 23, "mech", 83),
    ("Ishita", 21, "cse", 64),
    ("Vikram", 20, "ece", 87),
]


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db(reset=False):
    """Creates the students table and fills it with sample data if it's empty."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        branch TEXT,
        marks INTEGER
    )
    """)

    if reset:
        cursor.execute("DELETE FROM students")

    count = cursor.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    if count == 0:
        cursor.executemany(
            "INSERT INTO students (name, age, branch, marks) VALUES (?, ?, ?, ?)",
            SAMPLE_STUDENTS
        )

    conn.commit()
    conn.close()
