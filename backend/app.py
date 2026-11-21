import os
import sqlite3
import logging
from pathlib import Path
from flask import Flask, request, jsonify, render_template

APP_DIR = Path(__file__).resolve().parent
DB_PATH = os.getenv("DATABASE_PATH", str(APP_DIR / "students.db"))

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("smart-campus")
app = Flask(__name__, template_folder="../frontend")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, course TEXT NOT NULL)")

init_db()

@app.route("/")
def home():
    with db() as conn:
        students = conn.execute("SELECT id, name, email, course FROM students ORDER BY id DESC").fetchall()
    return render_template("index.html", students=students)

@app.route("/api/students", methods=["GET", "POST"])
def students_api():
    if request.method == "GET":
        with db() as conn:
            records = conn.execute("SELECT id, name, email, course FROM students ORDER BY id DESC").fetchall()
        return jsonify([dict(r) for r in records])
    payload = request.get_json(silent=True) or request.form
    name, email, course = (str(payload.get(k, "")).strip() for k in ("name", "email", "course"))
    if not all((name, email, course)):
        return jsonify(error="name, email and course are required"), 400
    try:
        with db() as conn:
            cur = conn.execute("INSERT INTO students(name, email, course) VALUES (?, ?, ?)", (name, email, course))
            student_id = cur.lastrowid
        logger.info("Student registration created id=%s", student_id)
        return jsonify(id=student_id, name=name, email=email, course=course), 201
    except sqlite3.IntegrityError:
        return jsonify(error="This email is already registered"), 409

@app.route("/health")
def health():
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="healthy", service="smart-campus"), 200
    except Exception as exc:
        logger.exception("Health check failed")
        return jsonify(status="unhealthy", error=str(exc)), 500

@app.route("/metrics")
def metrics():
    with db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    return (f"# HELP smart_campus_registered_students Number of registered students\n"
            f"# TYPE smart_campus_registered_students gauge\nsmart_campus_registered_students {count}\n"), 200, {"Content-Type": "text/plain; version=0.0.4"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))  # nosec B104 - required for Docker
