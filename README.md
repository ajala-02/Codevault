<div align="center">

# &lt;/&gt; CodeVault

### Your solved problems deserve a second brain.

**A private coding-problem tracker with active-recall reviews, built for deliberate practice.**

Built as a CS50 Final Project using Python, Flask, SQLite, Bootstrap, JavaScript, and Chart.js.

</div>

---

## About CodeVault

CodeVault is a web-based coding-problem tracking application for students and developers practicing DSA and competitive programming.

Users can save problems from platforms such as LeetCode, HackerRank, and Codeforces, record their own solution notes, track progress by difficulty and topic, and revisit older problems using a spaced-repetition review queue.

Unlike a normal list of solved links, CodeVault helps users remember **how** they solved a problem.

## Screenshots

### Dashboard

The dashboard shows total solved problems, difficulty breakdown, topics covered, recently solved problems, and the number of problems due for review.

![CodeVault Dashboard](assets/dashboard.png)

### Review Mode

Review Mode encourages active recall. Users first try to remember the solution, reveal their saved notes when needed, and then mark the problem as reviewed.

![CodeVault Review Mode](assets/review-mode.png)

### Statistics

The statistics page displays a Chart.js difficulty chart and topic-wise problem totals.

![CodeVault Statistics](assets/statistics.png)

## Features

- Secure user registration, login, and logout
- Unique usernames
- Password hashing with Werkzeug
- Session-based authentication
- Private problem vault for every user
- Add coding problems with a name, platform, URL, difficulty, topic, solved date, and personal notes
- View, edit, and delete saved problems
- Search problems by name
- Filter problems by difficulty and topic
- Dashboard with Easy, Medium, Hard, topic, and recent-activity totals
- Statistics page with Chart.js visualizations
- Review Mode with spaced repetition
- User ownership checks on every problem route
- Validation for URLs, dates, required fields, and difficulty values

## Review Mode

Review Mode is the main unique feature of CodeVault.

When a user adds a solved problem, CodeVault schedules it for review. During a review session, the user tries to recall the approach before revealing saved notes.

After the problem is marked as reviewed, the next review date is scheduled farther in the future:

```text
1 day → 3 days → 7 days → 14 days → 30 days → 60 days
```

This system is inspired by spaced repetition and active recall, helping users retain important DSA patterns over time.

## Tech Stack

| Technology | Purpose |
| --- | --- |
| Python | Backend programming language |
| Flask | Web framework, routing, and sessions |
| SQLite | Local relational database |
| HTML / Jinja | Dynamic page templates |
| Bootstrap | Responsive layout and components |
| CSS | Custom CodeVault design |
| JavaScript | Search, filters, and delete confirmation |
| Chart.js | Difficulty statistics chart |
| Werkzeug | Password hashing |

## Project Structure

```text
Codevault/
├── app.py                  # Flask routes, validation, database setup
├── helpers.py              # login_required helper
├── requirements.txt        # Python dependencies
├── seed_demo.py            # Creates demo problem data
├── reset_demo_database.py  # Rebuilds local demo database
├── static/
│   ├── styles.css          # Custom styling
│   └── script.js           # Search, filtering, delete confirmation
├── templates/              # Jinja HTML templates
├── tests/
│   └── test_app.py         # Automated tests
└── assets/                 # README screenshots
```

## Database Design

### `users`

```text
id
username
hash
```

### `problems`

```text
id
user_id
name
platform
url
difficulty
topic
date_solved
notes
created_at
review_count
review_interval
last_reviewed
next_review
```

Each problem belongs to one user through `user_id`.

## Security

- Passwords are hashed; plaintext passwords are never stored.
- Authenticated pages require a valid session.
- Every problem query checks the signed-in user ID.
- Users cannot view, edit, review, or delete another user’s problems.
- Parameterized SQL queries help prevent SQL injection.
- Problem URLs, dates, required fields, and difficulty values are validated.

## Run Locally

```bash
git clone https://github.com/ajala-02/Codevault.git
cd Codevault

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m flask --app app run
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

## Demo Data

Create a demo account with sample coding problems:

```bash
python3 seed_demo.py
```

Demo login:

```text
Username: demo_user
Password: demo1234
```

To remove all local data and recreate 50 clearly labeled demo accounts:

```bash
python3 reset_demo_database.py
```

> The demo accounts are only local sample data. CodeVault does not publicly display other users because all vaults are private.

## Tests

Run automated tests with:

```bash
python3 -m unittest discover -s tests -v
```

The tests verify spaced-repetition intervals, review completion, and user ownership protection.

## Design Philosophy

CodeVault intentionally uses Flask, SQLite, Bootstrap, vanilla JavaScript, and Chart.js. The project stays understandable and explainable for a CS50 student while avoiding unnecessary frameworks, AI APIs, scraping, social features, and external services.

## AI Assistance Disclosure

AI assistance was used to help draft portions of this project. The author reviewed, adapted, and understands the submitted code. Generated or adapted source files include comments acknowledging that assistance, in line with the CS50 Final Project policy.

---

<div align="center">

Built for the satisfying moment when a hard problem finally clicks. ✦

</div>
