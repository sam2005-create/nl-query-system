import sqlite3

DB_NAME = "students.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
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

    cursor.execute("DELETE FROM students")

    data = [
        ("Sam", 20, "cse", 85),
        ("Rahul", 21, "ece", 78),
        ("Ankit", 19, "cse", 92),
        ("Priya", 20, "mech", 74),
        ("Neha", 22, "cse", 88)
    ]

    cursor.executemany(
        "INSERT INTO students (name, age, branch, marks) VALUES (?, ?, ?, ?)",
        data
    )

    conn.commit()
    conn.close()