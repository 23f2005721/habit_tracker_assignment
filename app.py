import sqlite3
from datetime import date
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for

from streak import calculate_streak, parse_completion_dates

app = Flask(__name__)
DATABASE = Path(__file__).parent / "habits.db"


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS habit_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completion_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
            UNIQUE (habit_id, completion_date)
        )
        """
    )
    db.commit()
    db.close()


def habit_with_streak(db, habit_row, today: str):
    completions = db.execute(
        "SELECT completion_date FROM habit_completions WHERE habit_id = ?",
        (habit_row["id"],),
    ).fetchall()
    dates = parse_completion_dates(completions)
    return {
        "id": habit_row["id"],
        "name": habit_row["name"],
        "created_at": habit_row["created_at"],
        "streak": calculate_streak(dates),
        "completed_today": today in {row["completion_date"] for row in completions},
    }


@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    today = date.today().isoformat()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            try:
                db.execute("INSERT INTO habits (name) VALUES (?)", (name,))
                db.commit()
            except sqlite3.IntegrityError:
                pass

    habits = [
        habit_with_streak(db, row, today)
        for row in db.execute(
            "SELECT id, name, created_at FROM habits ORDER BY id DESC"
        ).fetchall()
    ]

    return render_template("index.html", habits=habits)


@app.post("/complete/<int:habit_id>")
def complete_habit(habit_id):
    db = get_db()
    today = date.today().isoformat()
    try:
        db.execute(
            "INSERT INTO habit_completions (habit_id, completion_date) VALUES (?, ?)",
            (habit_id, today),
        )
        db.commit()
    except sqlite3.IntegrityError:
        pass
    return redirect(url_for("index"))


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
