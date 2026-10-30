import re
from db import get_connection

BRANCHES = ["cse", "ece", "mech"]

# words people use for > and <, longest first so "greater than" wins over "over"
COMPARE = {
    "greater than": ">",
    "more than": ">",
    "above": ">",
    "over": ">",
    "less than": "<",
    "below": "<",
    "under": "<",
}
OPS = "|".join(sorted(COMPARE, key=len, reverse=True))

FIELD_WORDS = {
    "marks": r"marks|mark|scored|score|scoring",
    "age": r"age|aged",
}


def find_number_filter(query, field):
    words = FIELD_WORDS[field]

    # "marks above 80", "scored more than 80", "age is below 21"
    m = re.search(rf"\b(?:{words})\s+(?:is\s+|are\s+)?({OPS})\s+(\d+)", query)
    if m:
        return f"{field} {COMPARE[m.group(1)]} {m.group(2)}"

    # "below age 21", "above marks 80"
    m = re.search(rf"\b({OPS})\s+(?:the\s+)?(?:{words})\s+(?:of\s+)?(\d+)", query)
    if m:
        return f"{field} {COMPARE[m.group(1)]} {m.group(2)}"

    if field == "age":
        m = re.search(r"\b(older|younger) than (\d+)", query)
        if m:
            op = ">" if m.group(1) == "older" else "<"
            return f"age {op} {m.group(2)}"

    return None


def build_where(query):
    conditions = []

    branches = [b for b in BRANCHES if re.search(rf"\b{b}\b", query)]
    if len(branches) == 1:
        conditions.append(f"branch = '{branches[0]}'")
    elif branches:
        names = ", ".join(f"'{b}'" for b in branches)
        conditions.append(f"branch IN ({names})")

    for field in ("marks", "age"):
        cond = find_number_filter(query, field)
        if cond:
            conditions.append(cond)

    if not conditions:
        return ""
    return " WHERE " + " AND ".join(conditions)


def nl_to_sql(query):
    """Turns a plain English question into SQL. Returns None if it can't."""
    query = query.lower().strip()
    where = build_where(query)

    if "average" in query or "avg" in query:
        field = "age" if re.search(r"\b(?:average|avg) age\b", query) else "marks"
        return f"SELECT ROUND(AVG({field}), 2) AS average_{field} FROM students{where}"

    if re.search(r"\b(how many|count|number of)\b", query):
        return f"SELECT COUNT(*) AS students FROM students{where}"

    # top / bottom N by marks; the filters still apply
    top = re.search(r"\b(top|bottom|lowest)\s+(\d+)", query)
    if top:
        order = "DESC" if top.group(1) == "top" else "ASC"
        return f"SELECT * FROM students{where} ORDER BY marks {order} LIMIT {top.group(2)}"

    if re.search(r"\b(top|highest|best)\b", query):
        return f"SELECT * FROM students{where} ORDER BY marks DESC LIMIT 3"

    if re.search(r"\b(bottom|lowest|worst)\b", query):
        return f"SELECT * FROM students{where} ORDER BY marks ASC LIMIT 3"

    if where or "student" in query:
        return f"SELECT * FROM students{where}"

    return None


def execute_sql(sql):
    """Runs the query and returns (column names, rows)."""
    conn = get_connection()
    try:
        cursor = conn.execute(sql)
        columns = [col[0] for col in cursor.description]
        return columns, cursor.fetchall()
    finally:
        conn.close()
