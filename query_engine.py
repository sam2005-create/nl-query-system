import re
from db import get_connection


def nl_to_sql(query):
    query = query.lower().strip()

    base = "SELECT * FROM students"
    conditions = []

    # 🔹 Branch detection
    if "cse" in query:
        conditions.append("branch='cse'")
    elif "ece" in query:
        conditions.append("branch='ece'")
    elif "mech" in query:
        conditions.append("branch='mech'")

    # 🔹 Marks condition
    marks_match = re.search(r'marks (above|greater than|below|less than) (\d+)', query)
    if marks_match:
        condition = marks_match.group(1)
        value = marks_match.group(2)

        if condition in ["above", "greater than"]:
            conditions.append(f"marks > {value}")
        elif condition in ["below", "less than"]:
            conditions.append(f"marks < {value}")

    # 🔹 Age condition
    age_match = re.search(r'age (above|greater than|below|less than) (\d+)', query)
    if age_match:
        condition = age_match.group(1)
        value = age_match.group(2)

        if condition in ["above", "greater than"]:
            conditions.append(f"age > {value}")
        elif condition in ["below", "less than"]:
            conditions.append(f"age < {value}")

    # 🔹 Top N students (dynamic)
    top_match = re.search(r'top (\d+)', query)
    if top_match:
        limit = top_match.group(1)
        return f"{base} ORDER BY marks DESC LIMIT {limit}"

    # 🔹 Default top (if just "top students")
    if "top" in query or "highest" in query:
        return base + " ORDER BY marks DESC LIMIT 3"

    # 🔹 Average
    if "average" in query:
        return "SELECT AVG(marks) FROM students"

    # 🔹 Build WHERE clause
    if conditions:
        return base + " WHERE " + " AND ".join(conditions)

    # 🔹 Default query
    if "student" in query:
        return base

    return None


def execute_sql(sql):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        return str(e)
    finally:
        conn.close()