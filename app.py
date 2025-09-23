""" Flask + SQLite backend for CampusCircle """

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import os
from datetime import datetime

DB_NAME = os.environ.get("DB_NAME", "alumni.db")

app = Flask(__name__)
CORS(app)

# ----------------- Database -----------------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            city TEXT,
            branch TEXT,
            year INTEGER,
            current_job TEXT,
            current_company TEXT,
            mobile TEXT,
            email TEXT UNIQUE,
            linkedin TEXT
        )
        """)
    print("✅ Database initialized")

init_db()

# ----------------- Routes -----------------

@app.route("/", methods=["GET"])
def health():
    return jsonify({"message": "CampusCircle backend running"})


# Get all alumni
@app.route("/alumni", methods=["GET"])
def get_alumni():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alumni")
        rows = cursor.fetchall()
        alumni = [
            {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "city": row[3],
                "branch": row[4],
                "year": row[5],
                "current_job": row[6],
                "current_company": row[7],
                "mobile": row[8],
                "email": row[9],
                "linkedin": row[10],
            }
            for row in rows
        ]
    return jsonify(alumni)


# Get single alumni
@app.route("/alumni/<int:alumni_id>", methods=["GET"])
def get_alumni_by_id(alumni_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alumni WHERE id=?", (alumni_id,))
        row = cursor.fetchone()
    if row:
        alumni = {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "city": row[3],
            "branch": row[4],
            "year": row[5],
            "current_job": row[6],
            "current_company": row[7],
            "mobile": row[8],
            "email": row[9],
            "linkedin": row[10],
        }
        return jsonify(alumni)
    return jsonify({"error": "Alumni not found"}), 404


# Add new alumni
@app.route("/alumni", methods=["POST"])
def add_alumni():
    data = request.json
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO alumni (name, age, city, branch, year, current_job, current_company, mobile, email, linkedin)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                data.get("name"),
                data.get("age"),
                data.get("city"),
                data.get("branch"),
                data.get("year"),
                data.get("current_job"),
                data.get("current_company"),
                data.get("mobile"),
                data.get("email"),
                data.get("linkedin"),
            ),
        )
        conn.commit()
        alumni_id = cursor.lastrowid
    return jsonify({"message": "Alumni added", "id": alumni_id})


# Update alumni
@app.route("/alumni/<int:alumni_id>", methods=["PUT"])
def update_alumni(alumni_id):
    data = request.json
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE alumni SET name=?, age=?, city=?, branch=?, year=?, current_job=?, 
               current_company=?, mobile=?, email=?, linkedin=? WHERE id=?""",
            (
                data.get("name"),
                data.get("age"),
                data.get("city"),
                data.get("branch"),
                data.get("year"),
                data.get("current_job"),
                data.get("current_company"),
                data.get("mobile"),
                data.get("email"),
                data.get("linkedin"),
                alumni_id,
            ),
        )
        conn.commit()
    return jsonify({"message": "Alumni updated"})


# Delete alumni
@app.route("/alumni/<int:alumni_id>", methods=["DELETE"])
def delete_alumni(alumni_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alumni WHERE id=?", (alumni_id,))
        conn.commit()
    return jsonify({"message": "Alumni deleted"})


# ----------------- Main -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
