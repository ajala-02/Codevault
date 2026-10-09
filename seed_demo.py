"""Create a safe, repeatable demo account with sample CodeVault data.

This utility was drafted with AI assistance and reviewed by the project author.
Run once with: python3 seed_demo.py
"""

from datetime import date, timedelta

from werkzeug.security import generate_password_hash

from app import app, get_db, init_db


DEMO_USERNAME = "demo_user"
DEMO_PASSWORD = "demo1234"


def sample_problems():
    """Return varied records that make the dashboard and Review Mode useful."""
    today = date.today()
    return [
        ("Two Sum", "LeetCode", "https://leetcode.com/problems/two-sum/", "Easy", "Arrays", 48, 2, -2, "Store each number in a hash map and look up the complement. O(n) time."),
        ("Valid Parentheses", "LeetCode", "https://leetcode.com/problems/valid-parentheses/", "Easy", "Stacks", 42, 1, 0, "Push opening brackets. Every closing bracket must match the latest opening bracket."),
        ("Binary Search", "LeetCode", "https://leetcode.com/problems/binary-search/", "Easy", "Binary Search", 36, 2, 6, "Keep left and right pointers; compare the middle value each time."),
        ("Product of Array Except Self", "LeetCode", "https://leetcode.com/problems/product-of-array-except-self/", "Medium", "Arrays", 31, 1, -1, "Build prefix products, then multiply them by suffix products without division."),
        ("Longest Substring Without Repeating Characters", "LeetCode", "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "Medium", "Sliding Window", 26, 2, 4, "Move the left pointer after a repeated character. Track the last position of each character."),
        ("Number of Islands", "LeetCode", "https://leetcode.com/problems/number-of-islands/", "Medium", "Graphs", 22, 0, -3, "Use DFS to visit every connected land cell and mark it as visited."),
        ("Coin Change", "LeetCode", "https://leetcode.com/problems/coin-change/", "Medium", "Dynamic Programming", 18, 1, 0, "dp[amount] is the fewest coins needed. Start with an impossible large value."),
        ("Merge Intervals", "LeetCode", "https://leetcode.com/problems/merge-intervals/", "Medium", "Intervals", 15, 1, 8, "Sort by starting point and merge when the next interval overlaps the current one."),
        ("LRU Cache", "LeetCode", "https://leetcode.com/problems/lru-cache/", "Medium", "Design", 12, 0, -2, "A hash map plus a doubly linked list gives O(1) get and put operations."),
        ("Trapping Rain Water", "LeetCode", "https://leetcode.com/problems/trapping-rain-water/", "Hard", "Two Pointers", 9, 0, -1, "Move the shorter side inward while tracking the maximum height from both ends."),
        ("Median of Two Sorted Arrays", "LeetCode", "https://leetcode.com/problems/median-of-two-sorted-arrays/", "Hard", "Binary Search", 6, 0, 1, "Binary-search the partition in the smaller array until both left halves are valid."),
        ("Word Break", "LeetCode", "https://leetcode.com/problems/word-break/", "Medium", "Dynamic Programming", 3, 0, 1, "For each position, check whether an earlier reachable position creates a dictionary word."),
    ]


def seed_demo_data():
    """Create one demo account and skip records already inserted on earlier runs."""
    init_db()
    with app.app_context():
        db = get_db()
        user = db.execute("SELECT id FROM users WHERE username = ?", (DEMO_USERNAME,)).fetchone()
        if user is None:
            cursor = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                (DEMO_USERNAME, generate_password_hash(DEMO_PASSWORD, method="pbkdf2:sha256")),
            )
            user_id = cursor.lastrowid
        else:
            user_id = user["id"]

        existing_names = {
            row["name"]
            for row in db.execute("SELECT name FROM problems WHERE user_id = ?", (user_id,)).fetchall()
        }
        added = 0
        for name, platform, url, difficulty, topic, days_ago, reviews, days_until_review, notes in sample_problems():
            if name in existing_names:
                continue
            solved_on = date.today() - timedelta(days=days_ago)
            last_reviewed = date.today() - timedelta(days=max(days_until_review + 1, 1)) if reviews else None
            next_review = date.today() + timedelta(days=days_until_review)
            db.execute(
                """INSERT INTO problems
                   (user_id, name, platform, url, difficulty, topic, date_solved, notes,
                    review_count, review_interval, last_reviewed, next_review)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (user_id, name, platform, url, difficulty, topic, solved_on.isoformat(), notes,
                 reviews, 7 if reviews else 1,
                 last_reviewed.isoformat() if last_reviewed else None, next_review.isoformat()),
            )
            added += 1
        db.commit()
    print(f"Demo account ready: {DEMO_USERNAME} / {DEMO_PASSWORD} ({added} sample problems added)")


if __name__ == "__main__":
    seed_demo_data()
