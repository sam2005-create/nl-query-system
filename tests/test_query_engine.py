import pytest

import db
from query_engine import nl_to_sql, execute_sql


@pytest.fixture
def sample_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_NAME", str(tmp_path / "test.db"))
    db.init_db()


def names(sql):
    columns, rows = execute_sql(sql)
    i = columns.index("name")
    return sorted(row[i] for row in rows)


def test_filters():
    assert nl_to_sql("students with marks above 80") == "SELECT * FROM students WHERE marks > 80"
    assert nl_to_sql("cse students below age 21") == "SELECT * FROM students WHERE branch = 'cse' AND age < 21"
    assert nl_to_sql("students who scored more than 80") == "SELECT * FROM students WHERE marks > 80"
    assert nl_to_sql("ece students older than 20") == "SELECT * FROM students WHERE branch = 'ece' AND age > 20"


def test_top_n_keeps_filters():
    assert nl_to_sql("top 3 cse students") == \
        "SELECT * FROM students WHERE branch = 'cse' ORDER BY marks DESC LIMIT 3"
    assert nl_to_sql("top students") == "SELECT * FROM students ORDER BY marks DESC LIMIT 3"


def test_aggregates_keep_filters():
    assert nl_to_sql("average marks of cse students") == \
        "SELECT ROUND(AVG(marks), 2) AS average_marks FROM students WHERE branch = 'cse'"
    assert nl_to_sql("average age") == "SELECT ROUND(AVG(age), 2) AS average_age FROM students"
    assert nl_to_sql("how many mech students") == \
        "SELECT COUNT(*) AS students FROM students WHERE branch = 'mech'"


def test_unknown_question():
    assert nl_to_sql("what's the weather") is None


def test_results_from_sample_data(sample_db):
    assert names(nl_to_sql("cse students below age 21")) == ["Ankit", "Kavya", "Sam"]
    assert names(nl_to_sql("top 2 ece students")) == ["Sneha", "Vikram"]

    columns, rows = execute_sql(nl_to_sql("how many students"))
    assert columns == ["students"]
    assert rows[0][0] == len(db.SAMPLE_STUDENTS)
