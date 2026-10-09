# CodeVault

CodeVault is a personal coding-problem tracker built as a CS50 Final Project. It helps users keep a private record of solved DSA and coding problems, identify their progress, and actively revisit old solutions using spaced repetition.

> **AI assistance disclosure:** AI assistance was used to help draft portions of this project. The author reviewed, adapted, and understands the submitted code. Source files containing generated or adapted code are marked with comments, in line with the CS50 Final Project policy.

## Highlights

- Secure registration, login, and logout with Werkzeug password hashing
- Private, per-user problem records protected on every route
- Add, view, update, and delete coding problems
- Dashboard totals for difficulty, topics, and recent activity
- Browser-side search and filtering by name, difficulty, and topic
- Statistics page with a Chart.js difficulty chart and topic totals
- Review Mode with an SM-2-inspired spaced-repetition schedule for active recall
- Input validation for required data, dates, difficulties, and HTTP(S) URLs
- SQLite indexes for fast problem lists and review queues

## Tech stack

- Python and Flask
- SQLite
- HTML, Bootstrap, and custom CSS
- Vanilla JavaScript
- Chart.js

## Project structure

- `app.py` contains the Flask routes, SQLite initialization, validation, review scheduler, and ownership checks.
- `helpers.py` contains the `login_required` decorator.
- `templates/` contains the Jinja HTML pages.
- `static/styles.css` contains the responsive custom styling.
- `static/script.js` contains filtering and delete confirmation behaviour.
- `codevault.db` is created automatically the first time the application runs.
- `seed_demo.py` creates a separate account with sample data for demonstrations.
- `tests/` contains automated tests for the review schedule and access control.

## Run locally or in the CS50 Codespace

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Open the address Flask prints in the terminal. For a Codespace, use its forwarded port preview. To use a non-default session key, set `SECRET_KEY` before starting Flask:

```bash
export SECRET_KEY="a-long-random-secret"
```

## Demo data

To populate a separate demo account with twelve sample problems, run:

```bash
python3 seed_demo.py
```

Then log in with username `demo_user` and password `demo1234`. The script is safe to run more than once; it does not duplicate the sample problems or modify other accounts.

## Tests

Run the automated test suite with:

```bash
python3 -m unittest discover -s tests
```

The tests check the expanding review intervals, completion of a review, and that users cannot access each other's problems.

## Design notes

SQLite holds two tables: `users` (`id`, `username`, `hash`) and `problems` (`id`, `user_id`, `name`, `platform`, `url`, `difficulty`, `topic`, `date_solved`, `notes`, `created_at`, plus review fields). Review Mode uses `review_count`, `review_interval`, `last_reviewed`, and `next_review`. After a review, it schedules the next session after 1, 3, 7, 14, 30, or 60 days. Every problem query uses both its ID and the signed-in `user_id`, so one user cannot read, edit, or delete another user's records.

The application intentionally uses only Flask, SQLite, Bootstrap, vanilla JavaScript, and Chart.js to keep the project approachable for a CS50 student. The database and virtual environment are intentionally excluded from Git; every fresh copy creates its own database when the application runs.
