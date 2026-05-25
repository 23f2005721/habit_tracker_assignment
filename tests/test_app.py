import unittest
from datetime import date, timedelta

from app import app, get_db, init_db


class HabitStreakAppTests(unittest.TestCase):
    def setUp(self):
        init_db()
        self.client = app.test_client()

    def _habit_id(self, name: str) -> int:
        with app.app_context():
            row = get_db().execute(
                "SELECT id FROM habits WHERE name = ?", (name,)
            ).fetchone()
            return row["id"]

    def test_complete_today_increases_streak(self):
        self.client.post("/", data={"name": "Read"}, follow_redirects=True)
        habit_id = self._habit_id("Read")

        self.client.post(f"/complete/{habit_id}", follow_redirects=True)
        response = self.client.get("/")

        self.assertIn(b"Streak: 1", response.data)
        self.assertIn(b"Done today", response.data)

    def test_five_day_streak_displayed(self):
        self.client.post("/", data={"name": "Exercise"}, follow_redirects=True)
        habit_id = self._habit_id("Exercise")

        with app.app_context():
            db = get_db()
            for i in range(5):
                d = (date.today() - timedelta(days=4 - i)).isoformat()
                db.execute(
                    "INSERT INTO habit_completions (habit_id, completion_date) VALUES (?, ?)",
                    (habit_id, d),
                )
            db.commit()

        response = self.client.get("/")
        self.assertIn(b"Streak: 5", response.data)


if __name__ == "__main__":
    unittest.main()
