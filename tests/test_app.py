"""Automated checks for CodeVault's authentication and review scheduler.

Tests were drafted with AI assistance and reviewed by the project author.
Run with: python3 -m unittest discover -s tests
"""

import os
import sqlite3
import tempfile
import unittest
from datetime import date
from pathlib import Path

import app as codevault


class CodeVaultTestCase(unittest.TestCase):
    def setUp(self):
        handle, database_name = tempfile.mkstemp(suffix=".db")
        os.close(handle)
        os.unlink(database_name)
        self.database_path = Path(database_name)
        codevault.DATABASE = self.database_path
        codevault.app.config.update(TESTING=True, SECRET_KEY="test-secret")
        codevault.init_db()
        self.client = codevault.app.test_client()

    def tearDown(self):
        if self.database_path.exists():
            self.database_path.unlink()

    def register(self, username, password="password1"):
        return self.client.post(
            "/register",
            data={"username": username, "password": password, "confirmation": password},
        )

    def add_problem(self, name="Two Sum"):
        return self.client.post(
            "/add",
            data={
                "name": name,
                "platform": "LeetCode",
                "url": "https://leetcode.com/problems/two-sum/",
                "difficulty": "Easy",
                "topic": "Arrays",
                # A past date makes the first scheduled review due immediately.
                "date_solved": "2020-01-01",
                "notes": "Use a hash map.",
            },
        )

    def test_schedule_intervals_expand(self):
        start = date(2026, 1, 1)
        self.assertEqual(codevault.next_review_date(0, start), ("2026-01-02", 1))
        self.assertEqual(codevault.next_review_date(1, start), ("2026-01-04", 3))
        self.assertEqual(codevault.next_review_date(2, start), ("2026-01-08", 7))

    def test_due_problem_can_be_reviewed(self):
        self.register("alice")
        self.add_problem()

        queue = self.client.get("/review")
        self.assertEqual(queue.status_code, 200)
        self.assertIn(b"Two Sum", queue.data)

        response = self.client.post("/review/1")
        self.assertEqual(response.status_code, 302)
        connection = sqlite3.connect(self.database_path)
        count, interval, last_reviewed = connection.execute(
            "SELECT review_count, review_interval, last_reviewed FROM problems WHERE id = 1"
        ).fetchone()
        connection.close()
        self.assertEqual((count, interval), (1, 3))
        self.assertEqual(last_reviewed, date.today().isoformat())

    def test_users_cannot_review_each_others_problem(self):
        self.register("alice")
        self.add_problem()
        self.client.get("/logout")
        self.register("bob")

        self.assertEqual(self.client.get("/problem/1").status_code, 404)
        self.assertEqual(self.client.post("/review/1").status_code, 404)


if __name__ == "__main__":
    unittest.main()
