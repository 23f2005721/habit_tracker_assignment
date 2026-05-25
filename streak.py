from datetime import date, timedelta


def calculate_streak(completion_dates: set[date]) -> int:
    """Return consecutive completion days ending on the most recent completion."""
    if not completion_dates:
        return 0

    streak = 0
    day = max(completion_dates)
    while day in completion_dates:
        streak += 1
        day -= timedelta(days=1)
    return streak


def dates_from_rows(rows) -> set[date]:
    return {date.fromisoformat(row["completion_date"]) for row in rows}
