import sqlite3

from flask import Flask, render_template, request, jsonify
from db import init_db
from query_engine import nl_to_sql, execute_sql

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json(silent=True)

    if not data or not data.get("query", "").strip():
        return jsonify({"error": "Type a question first."}), 400

    user_query = data["query"]
    sql = nl_to_sql(user_query)

    if not sql:
        return jsonify({"error": "Sorry, I couldn't understand that. Try something like 'cse students with marks above 80'."}), 400

    try:
        columns, rows = execute_sql(sql)
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}", "sql": sql}), 500

    return jsonify({
        "input": user_query,
        "sql": sql,
        "columns": columns,
        "rows": rows
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
