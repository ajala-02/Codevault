"""Permanently reset local CodeVault data and create clearly labeled demo users.

This utility was drafted with AI assistance and reviewed by the project author.
Run: python3 reset_demo_database.py
"""

from werkzeug.security import generate_password_hash

from app import app, get_db, init_db


DEMO_PASSWORD = "demo-password"


def reset_and_seed():
    """Rebuild the local schema, then seed 50 non-real demo accounts."""
    with app.app_context():
        db = get_db()
        # This removes all local user data and any old, unused schema columns.
        db.execute("DROP TABLE IF EXISTS problems")
        db.execute("DROP TABLE IF EXISTS users")
        db.commit()

    init_db()
    with app.app_context():
        db = get_db()
        for number in range(1, 51):
            username = f"demo_account_{number:02d}"
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                (
                    username,
                    generate_password_hash(DEMO_PASSWORD, method="pbkdf2:sha256"),
                ),
            )
        db.commit()
    print("Database reset complete. Added 50 clearly labeled demo accounts.")


if __name__ == "__main__":
    reset_and_seed()
