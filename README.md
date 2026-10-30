# NL Query System

Ask a database questions in plain English and get the answer back as a table. Type "cse students below age 21" and the app turns it into SQL, runs it on a SQLite database and shows you both the query and the result.

Built with Python, Flask and SQLite, with a plain HTML/JS front end.

## What you can ask

The sample database has 12 students with a name, age, branch (cse, ece, mech) and marks.

| You type | SQL it runs |
| --- | --- |
| all students | `SELECT * FROM students` |
| students with marks above 80 | `... WHERE marks > 80` |
| cse students below age 21 | `... WHERE branch = 'cse' AND age < 21` |
| top 3 cse students | `... WHERE branch = 'cse' ORDER BY marks DESC LIMIT 3` |
| average marks of ece students | `SELECT ROUND(AVG(marks), 2) ... WHERE branch = 'ece'` |
| how many students scored above 85 | `SELECT COUNT(*) ... WHERE marks > 85` |

Filters work together, so you can mix a branch, a marks condition and an age condition in one question. It understands "above", "below", "more than", "less than", "over", "under", "older than" and "younger than".

## How it works

`query_engine.py` reads the question with a set of regex rules. It picks out the branch, any marks or age conditions, and whether you want a top/bottom list, an average or a count. Then it builds the SQL from those pieces. Numbers come straight from the regex match and branches from a fixed list, so user text never goes into the query directly.

If it can't make sense of a question, it says so instead of guessing.

## Running it

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000. The database file is created with sample data on the first run. To put the sample data back after changing it, run `python reset_db.py`.

## Tests

```bash
python -m pytest
```

## Limitations

It only knows the one `students` table and the phrasings above. Something like "students who did well" won't work. A possible next step is letting an LLM write the SQL from the table schema, with the rule-based parser kept as a fallback.
