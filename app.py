import sqlite3
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for

app = Flask(__name__)
DATABASE = Path(__file__).parent / "habits.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()
    db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            try:
                db.execute("INSERT INTO habits (name) VALUES (?)", (name,))
                db.commit()
            except sqlite3.IntegrityError:
                pass

    habits = db.execute(
        "SELECT id, name, created_at FROM habits ORDER BY id DESC"
    ).fetchall()

    return render_template("index.html", habits=habits)


@app.post("/delete/<int:habit_id>")
def delete_habit(habit_id):
    db = get_db()
    db.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    print("Habit Tracker running at http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
