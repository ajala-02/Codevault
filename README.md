<div align="center">

# </> CodeVault

### Your solved problems deserve a second brain.

A private coding-problem tracker that uses **spaced repetition** and **active recall**, so you actually remember how you solved it.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3BABC3?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

</div>
<div align="center">

<b>CS50x Final Project</b>
<br>
<b>Video Demo:</b> <a href="https://youtu.be/gg0ZCP6hcmU">https://youtu.be/gg0ZCP6hcmU</a>

</div>

## 💡 Why CodeVault?

Most of us solve a problem, feel great, and forget the approach two weeks later. A list of solved links doesn't fix that.

CodeVault saves your **own notes** and brings each problem back at the right time, so patterns stick instead of fading.

## 📸 Screenshots

### Dashboard
Your progress at a glance: totals, difficulty breakdown, topics covered, and what's due for review today.

![CodeVault Dashboard](assets/dashboard.png)

### Review Mode
Recall the approach first. Reveal your notes only when you need them.

![CodeVault Review Mode](assets/review-mode.png)

### Statistics
See where you're strong and where you're not, by difficulty and by topic.

![CodeVault Statistics](assets/statistics.png)

## ✨ Features

- 🔐 **Private vaults:** secure sign-up and login, and every user's problems stay theirs
- 📝 **Save problems** from LeetCode, HackerRank, Codeforces, or anywhere else, with your own notes
- 🔎 **Search and filter** by name, difficulty, or topic
- 📊 **Dashboard and stats** powered by Chart.js
- 🧠 **Review Mode** with spaced repetition, the heart of the app
- ✅ **Validated inputs** for URLs, dates, and required fields

## 🧠 How Review Mode Works

1. **Solve** a problem and save it with your notes.
2. **Recall** the approach from memory when it comes due.
3. **Reveal** your notes to check yourself.
4. **Mark reviewed** and the next review moves further out.

```text
1 day  →  3 days  →  7 days  →  14 days  →  30 days  →  60 days
```

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, Jinja, Bootstrap, CSS, JavaScript |
| Charts | Chart.js |
| Security | Werkzeug password hashing, session auth, parameterized SQL |

## 🔒 Under the Hood

- Passwords are hashed, never stored in plaintext
- Every query is scoped to the signed-in user, so no one can view, edit, review, or delete another user's problems
- Parameterized SQL queries protect against SQL injection

## 📁 Project Layout

```text
Codevault/
├── app.py          # Routes, validation, database setup
├── helpers.py      # Login helper
├── templates/      # Jinja pages
├── static/         # CSS and JavaScript
├── tests/          # Automated tests
└── assets/         # README screenshots
```

## 📂 Files and What They Do

- **app.py** is the core of the project. It defines every route (register, login, logout, dashboard, add, edit, delete, problem list, details, review, statistics), validates all user input, creates the SQLite tables, and contains the logic that schedules each problem's next review date.
- **helpers.py** holds the `login_required` decorator, which redirects anonymous visitors to the login page so private routes stay private.
- **templates/** contains the Jinja pages. They all extend one shared layout, so navigation and styling stay consistent across the app.
- **static/styles.css** is the custom design layered on top of Bootstrap. **static/script.js** handles live search, filtering, and delete confirmation in the browser.
- **seed_demo.py** and **reset_demo_database.py** create sample accounts and problems, so the app can be explored without typing in data by hand.
- **tests/test_app.py** contains automated tests for the review intervals, review completion, and the rule that users cannot review each other's problems.
- **assets/** holds the screenshots used in this README.

## 🧩 Design Choices

**Why Flask and SQLite?** CodeVault has a small, clear data model: users and the problems they own. SQLite needs no separate server and keeps setup to a few commands, and Flask keeps routing and sessions simple enough that I can explain every line.

**Why a fixed review ladder?** The goal is retention, not storage. The intervals of 1, 3, 7, 14, 30, and 60 days are predictable, easy to test, and easy to explain. I chose them over a more complex adaptive algorithm because a simple schedule is easier to verify and debug.

**Why active recall?** Review Mode hides the notes until the user chooses to reveal them. Trying to remember the solution first is what strengthens memory, so the interface forces that step instead of just showing the answer.

**Why plain JavaScript?** Search and filtering run in the browser with vanilla JavaScript, so results update instantly without extra requests and without adding a frontend framework.

**Why strict ownership checks?** Every vault is private, so every problem query includes the signed-in user's ID. A user who guesses another problem's URL gets nothing back, and a test covers this case.

**Why server-side validation?** The browser can be bypassed, so URLs, dates, required fields, and difficulty values are all checked again on the server before anything reaches the database.

## 🚀 Run Locally

```bash
git clone https://github.com/ajala-02/Codevault.git
cd Codevault

python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m flask --app app run
```

Then open **http://127.0.0.1:5000**.

Want sample data to explore? Run `python3 seed_demo.py` and log in with `demo_user` / `demo1234`.

## ✅ Tests

```bash
python3 -m unittest discover -s tests -v
```

Covers spaced-repetition intervals, review completion, and user ownership protection.

## 🤖 AI Assistance

AI tools were used to help draft portions of this project. I reviewed, adapted, and understand all of the submitted code.

## 👨‍💻 Author

**Ajala Nalawade**

- GitHub: [@ajala-02](https://github.com/ajala-02)
- LinkedIn: [your-linkedin-url](https://www.linkedin.com/in/ajala-nalawade02/?isSelfProfile=true)
- Email: ajala.nalawade@gmail.com

---

<div align="center">

Built for the satisfying moment when a hard problem finally clicks. ✦

</div>