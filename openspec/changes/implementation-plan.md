# Habit Streak — Implementation Plan

**Source spec:** `openspec/specs/habit-streak/spec.md`  
**Target app:** `habit_tracker/` (Flask + SQLite)

## Requirements summary

| ID | Requirement | Notes |
|----|-------------|-------|
| FR-1 | User can mark a habit complete | POST action per habit, one completion per calendar day |
| FR-2 | Completion date is stored | `HabitCompletion.completion_date` (DATE, UTC/local date) |
| FR-3 | Consecutive days increase streak | Count backward from latest completion without gaps |
| FR-4 | Missing a day resets streak | Gap in dates breaks the chain; new completions start at 1 |
| AC-1 | 5 consecutive days → streak = 5 | Verified by streak calculator + tests |
| AC-2 | Missing one day resets streak | Gap between completions limits streak to post-gap run |

## Database changes

Add table `habit_completions`:

```sql
CREATE TABLE habit_completions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    completion_date TEXT NOT NULL,  -- ISO date YYYY-MM-DD
    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE,
    UNIQUE (habit_id, completion_date)
);
```

- `habits` table unchanged (`id`, `name`, `created_at`).
- Deleting a habit removes its completions (CASCADE).

## Streak algorithm

1. Load distinct `completion_date` values for a habit.
2. Let `latest` = most recent completion date (or 0 streak if none).
3. Starting at `latest`, walk backward one day at a time while that date exists in the set.
4. Return the count of days walked.

**Examples:**

- Completions: Mon–Fri → streak **5**.
- Completions: Mon–Wed, skip Thu, Fri → streak **1** (only Fri).
- No completions → streak **0**.

## API / routes

| Method | Path | Purpose |
|--------|------|---------|
| GET/POST | `/` | List habits with streak; add habit (unchanged) |
| POST | `/complete/<habit_id>` | Record today’s completion (idempotent) |
| POST | `/delete/<habit_id>` | Delete habit + completions (unchanged path) |

## UI changes (`templates/index.html`)

- Show streak next to each habit: e.g. `Read — streak: 5`.
- Add **Complete today** button per habit (disabled or hidden if already completed today).
- Keep existing Add / Delete flows.

## File changes

| File | Action |
|------|--------|
| `streak.py` | New — `calculate_streak(dates)` + `today_iso()` helpers |
| `app.py` | Migration in `init_db`, complete route, streak in index query |
| `templates/index.html` | Streak display + complete button |
| `tests/test_streak.py` | Unit tests for streak logic |
| `openspec/tests/habit-streak-test-plan.md` | Manual + automated test documentation |

## Implementation order

1. [x] Plan document (this file)
2. [x] `streak.py` + unit tests
3. [x] `habit_completions` table + `init_db` migration
4. [x] `/complete/<id>` route
5. [x] Index: attach streak + `completed_today` per habit
6. [x] Template updates
7. [x] Test documentation in `openspec/tests/`
8. [x] Run tests and smoke-test in browser

## Risks / decisions

- **Timezone:** Use server local date (`date.today()`) for “today” — acceptable for a simple school/project app.
- **Double complete same day:** `UNIQUE (habit_id, completion_date)` + ignore duplicate insert.
- **Existing DBs:** `CREATE TABLE IF NOT EXISTS` only; no Alembic.

## Verification

- `python -m unittest tests.test_streak -v`
- Manual steps in `openspec/tests/habit-streak-test-plan.md`
