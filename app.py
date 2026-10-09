"""CodeVault, a personal coding-problem tracker.

Some boilerplate and explanatory comments in this student project were created
with AI assistance and reviewed/adapted by the project author.
"""

import os
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, abort, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required


BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "codevault.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-key-before-deploying")


def get_db():
    """Return one SQLite connection per request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the project tables if this is the first run."""
    db = sqlite3.connect(DATABASE)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            difficulty TEXT NOT NULL CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
            topic TEXT NOT NULL,
            date_solved TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            review_count INTEGER NOT NULL DEFAULT 0,
            review_interval INTEGER NOT NULL DEFAULT 1,
            last_reviewed TEXT,
            next_review TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        """
    )
    # Keep databases created before Review Mode compatible with the new feature.
    columns = {row[1] for row in db.execute("PRAGMA table_info(problems)")}
    migrations = {
        "review_count": "INTEGER NOT NULL DEFAULT 0",
        "review_interval": "INTEGER NOT NULL DEFAULT 1",
        "last_reviewed": "TEXT",
        "next_review": "TEXT",
    }
    for name, definition in migrations.items():
        if name not in columns:
            db.execute(f"ALTER TABLE problems ADD COLUMN {name} {definition}")
    # Existing saved problems begin their review cycle one day after being solved.
    db.execute(
        "UPDATE problems SET next_review = date(date_solved, '+1 day') WHERE next_review IS NULL"
    )
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_problems_user_solved ON problems (user_id, date_solved DESC)"
    )
    db.execute(
        "CREATE INDEX IF NOT EXISTS idx_problems_user_review ON problems (user_id, next_review)"
    )
    db.commit()
    db.close()


def valid_url(value):
    """Accept only complete HTTP(S) URLs, which are safe to link to."""
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def next_review_date(review_count, reviewed_on):
    """Return the next date in a small, explainable SM-2-inspired schedule.

    The intervals grow from 1 to 3, 7, 14, 30, then 60 days. This keeps the
    algorithm readable for a CS50 project while still supporting active recall.
    """
    intervals = (1, 3, 7, 14, 30, 60)
    interval = intervals[min(review_count, len(intervals) - 1)]
    return (reviewed_on + timedelta(days=interval)).isoformat(), interval


def validate_problem_form(form):
    """Return cleaned form data and an error message, if any."""
    data = {
        "name": form.get("name", "").strip(),
        "platform": form.get("platform", "").strip(),
        "url": form.get("url", "").strip(),
        "difficulty": form.get("difficulty", "").strip(),
        "topic": form.get("topic", "").strip(),
        "date_solved": form.get("date_solved", "").strip(),
        "notes": form.get("notes", "").strip(),
    }

    if not all(data[key] for key in ("name", "platform", "url", "difficulty", "topic", "date_solved")):
        return data, "Please complete every required field."
    if data["difficulty"] not in ("Easy", "Medium", "Hard"):
        return data, "Please select a valid difficulty."
    if not valid_url(data["url"]):
        return data, "Please enter a valid URL beginning with http:// or https://."
    try:
        datetime.strptime(data["date_solved"], "%Y-%m-%d")
    except ValueError:
        return data, "Please enter a valid date solved."
    return data, None


def get_owned_problem(problem_id):
    """Return a problem only when it belongs to the signed-in user."""
    try:
        problem_id = int(problem_id)
    except (TypeError, ValueError):
        abort(404)

    problem = get_db().execute(
        "SELECT * FROM problems WHERE id = ? AND user_id = ?",
        (problem_id, session["user_id"]),
    ).fetchone()
    if problem is None:
        abort(404)
    return problem


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirmation = request.form.get("confirmation", "")

        if not username or not password or not confirmation:
            flash("Please complete every field.", "danger")
        elif len(username) < 3 or len(username) > 30:
            flash("Username must be between 3 and 30 characters.", "danger")
        elif password != confirmation:
            flash("Passwords do not match.", "danger")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
        else:
            try:
                db = get_db()
                cursor = db.execute(
                    "INSERT INTO users (username, hash) VALUES (?, ?)",
                    # PBKDF2 is explicitly selected for compatibility with
                    # Python builds that do not include the optional scrypt support.
                    (username, generate_password_hash(password, method="pbkdf2:sha256")),
                )
                db.commit()
                session["user_id"] = cursor.lastrowid
                flash("Welcome to CodeVault!", "success")
                return redirect(url_for("index"))
            except sqlite3.IntegrityError:
                flash("That username is already taken.", "danger")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None or not check_password_hash(user["hash"], password):
            flash("Invalid username or password.", "danger")
        else:
            session["user_id"] = user["id"]
            flash("You are now logged in.", "success")
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    db = get_db()
    user_id = session["user_id"]
    counts = db.execute(
        """SELECT COUNT(*) AS total,
                  SUM(difficulty = 'Easy') AS easy,
                  SUM(difficulty = 'Medium') AS medium,
                  SUM(difficulty = 'Hard') AS hard,
                  COUNT(DISTINCT topic) AS topics
           FROM problems WHERE user_id = ?""",
        (user_id,),
    ).fetchone()
    recent = db.execute(
        "SELECT * FROM problems WHERE user_id = ? ORDER BY date_solved DESC, id DESC LIMIT 5",
        (user_id,),
    ).fetchall()
    due_reviews = db.execute(
        "SELECT COUNT(*) AS count FROM problems WHERE user_id = ? AND next_review <= ?",
        (user_id, date.today().isoformat()),
    ).fetchone()["count"]
    return render_template("index.html", counts=counts, recent=recent, due_reviews=due_reviews)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        data, error = validate_problem_form(request.form)
        if error:
            flash(error, "danger")
        else:
            db = get_db()
            first_review, first_interval = next_review_date(
                0, datetime.strptime(data["date_solved"], "%Y-%m-%d").date()
            )
            db.execute(
                """INSERT INTO problems
                (user_id, name, platform, url, difficulty, topic, date_solved, notes,
                 review_interval, next_review)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (session["user_id"], data["name"], data["platform"], data["url"],
                 data["difficulty"], data["topic"], data["date_solved"], data["notes"],
                 first_interval, first_review),
            )
            db.commit()
            flash("Problem added to your vault.", "success")
            return redirect(url_for("problems"))
        return render_template("add.html", problem=data)
    return render_template("add.html", problem={})


@app.route("/problems")
@login_required
def problems():
    rows = get_db().execute(
        "SELECT * FROM problems WHERE user_id = ? ORDER BY date_solved DESC, id DESC",
        (session["user_id"],),
    ).fetchall()
    topics = sorted({row["topic"] for row in rows}, key=str.lower)
    return render_template("problems.html", problems=rows, topics=topics)


@app.route("/problem/<int:problem_id>")
@login_required
def details(problem_id):
    return render_template("details.html", problem=get_owned_problem(problem_id))


@app.route("/review")
@login_required
def review():
    """Show up to ten problems scheduled for active recall today."""
    today = date.today().isoformat()
    due_problems = get_db().execute(
        """SELECT * FROM problems
           WHERE user_id = ? AND next_review <= ?
           ORDER BY next_review, review_count, id LIMIT 10""",
        (session["user_id"], today),
    ).fetchall()
    return render_template("review.html", problems=due_problems, today=today)


@app.route("/review/<int:problem_id>", methods=["POST"])
@login_required
def complete_review(problem_id):
    """Record a review and schedule the problem's next active-recall session."""
    problem = get_owned_problem(problem_id)
    today = date.today()
    new_count = problem["review_count"] + 1
    next_date, interval = next_review_date(new_count, today)
    db = get_db()
    db.execute(
        """UPDATE problems
           SET review_count = ?, review_interval = ?, last_reviewed = ?, next_review = ?
           WHERE id = ? AND user_id = ?""",
        (new_count, interval, today.isoformat(), next_date, problem["id"], session["user_id"]),
    )
    db.commit()
    flash(f"Review saved. This problem will return in {interval} days.", "success")
    return redirect(url_for("review"))


@app.route("/edit/<int:problem_id>", methods=["GET", "POST"])
@login_required
def edit(problem_id):
    problem = get_owned_problem(problem_id)
    if request.method == "POST":
        data, error = validate_problem_form(request.form)
        if error:
            flash(error, "danger")
            # The template also needs the original ID for its cancel link.
            data["id"] = problem["id"]
            return render_template("edit.html", problem=data)
        db = get_db()
        db.execute(
            """UPDATE problems SET name = ?, platform = ?, url = ?, difficulty = ?,
               topic = ?, date_solved = ?, notes = ? WHERE id = ? AND user_id = ?""",
            (*data.values(), problem["id"], session["user_id"]),
        )
        db.commit()
        flash("Problem updated.", "success")
        return redirect(url_for("details", problem_id=problem["id"]))
    return render_template("edit.html", problem=problem)


@app.route("/delete/<int:problem_id>", methods=["POST"])
@login_required
def delete(problem_id):
    problem = get_owned_problem(problem_id)
    db = get_db()
    db.execute("DELETE FROM problems WHERE id = ? AND user_id = ?", (problem["id"], session["user_id"]))
    db.commit()
    flash("Problem deleted.", "success")
    return redirect(url_for("problems"))


@app.route("/statistics")
@login_required
def statistics():
    db = get_db()
    user_id = session["user_id"]
    difficulty_rows = db.execute(
        "SELECT difficulty, COUNT(*) AS count FROM problems WHERE user_id = ? GROUP BY difficulty",
        (user_id,),
    ).fetchall()
    topic_rows = db.execute(
        "SELECT topic, COUNT(*) AS count FROM problems WHERE user_id = ? GROUP BY topic ORDER BY count DESC, topic",
        (user_id,),
    ).fetchall()
    difficulties = {row["difficulty"]: row["count"] for row in difficulty_rows}
    return render_template("statistics.html", difficulties=difficulties, topics=topic_rows)


init_db()


if __name__ == "__main__":
    app.run(debug=True)
