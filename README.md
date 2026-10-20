<div align="center">

# </> CodeVault

### Your solved problems deserve a second brain.

**A private coding-problem tracker with active-recall reviews, built for deliberate practice.**

[Features](#what-you-can-do) · [Quick Start](#quick-start) · [Review Mode](#review-mode) · [Tests](#tests)

</div>

---

Most coding platforms remember whether you solved a problem. CodeVault remembers what *you* learned from it.

Save a problem with your own notes, track progress across topics and difficulties, and let the review queue bring old solutions back before they fade.

> · Built with Python, Flask, SQLite, Bootstrap, JavaScript, and Chart.js.

## What You Can Do

| Feature | Description |
| --- | --- |
| 🔐 **Private Vault** | Register, log in, and keep every problem record private. |
| ➕ **Problem Journal** | Save title, platform, URL, difficulty, topic, solved date, and notes. |
| 🔎 **Search & Filter** | Search by name and filter by difficulty or topic. |
| 📊 **Statistics** | Track solved problems by difficulty and topic. |
| 🧠 **Review Mode** | Revisit old problems using spaced repetition. |
| ✏️ **Full Control** | View, edit, or delete your saved problems anytime. |

## Review Mode

Review Mode is CodeVault’s main unique feature.

Instead of becoming a list of old solved links, CodeVault helps you actively remember your approaches.

1. Add a solved problem.
2. CodeVault schedules its first review for the next day.
3. Open **Review Mode** and try to recall the solution before opening your notes.
4. Mark the problem as reviewed.
5. CodeVault schedules the next review farther in the future.

The review schedule expands through:

```text
1 → 3 → 7 → 14 → 30 → 60 days
