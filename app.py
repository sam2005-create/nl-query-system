from flask import Flask, render_template, request, jsonify
from query_engine import nl_to_sql, execute_sql

app = Flask(__name__)

# Home route → loads HTML page
@app.route("/")
def home():
    return render_template("index.html")


# API route → handles user query
@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "No query provided"})

    user_query = data["query"]

    # Convert NL → SQL
    sql = nl_to_sql(user_query)

    if not sql:
        return jsonify({"error": "Query not understood"})

    # Execute SQL
    result = execute_sql(sql)

    return jsonify({
        "input": user_query,
        "sql": sql,
        "result": result
    })


# Run server
if __name__ == "__main__":
    app.run(debug=True)