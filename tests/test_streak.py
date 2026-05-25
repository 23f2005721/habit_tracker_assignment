import unittest
from datetime import date, timedelta

from streak import calculate_streak


class StreakCalculationTests(unittest.TestCase):
    def test_empty_returns_zero(self):
        self.assertEqual(calculate_streak(set()), 0)

    def test_single_day(self):
        self.assertEqual(calculate_streak({date(2026, 5, 25)}), 1)

    def test_five_consecutive_days(self):
        start = date(2026, 5, 21)
        days = {start + timedelta(days=i) for i in range(5)}
        self.assertEqual(calculate_streak(days), 5)

    def test_gap_resets_streak(self):
        mon = date(2026, 5, 19)
        tue = date(2026, 5, 20)
        wed = date(2026, 5, 21)
        fri = date(2026, 5, 23)
        self.assertEqual(calculate_streak({mon, tue, wed, fri}), 1)

    def test_non_contiguous_ending_chain(self):
        d1 = date(2026, 5, 10)
        d2 = date(2026, 5, 11)
        d3 = date(2026, 5, 12)
        self.assertEqual(calculate_streak({d1, d3}), 1)
        self.assertEqual(calculate_streak({d1, d2, d3}), 3)


if __name__ == "__main__":
    unittest.main()
