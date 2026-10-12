import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, jsonify
from psycopg2.extras import RealDictCursor

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)


# Database connection helper using the Neon URL
def get_db_connection():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set.")
    return psycopg2.connect(database_url)


def get_latest_expenses(limit: int = 10):
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM expenses ORDER BY id DESC LIMIT %s;", (limit,))
        expenses = cur.fetchall()
        return expenses
    finally:
        conn.close()


# Route to get the latest 10 expenses
@app.route("/api/expenses/latest", methods=["GET"])
def latest_expenses_route():
    try:
        expenses = get_latest_expenses(limit=10)
        return jsonify(expenses)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

