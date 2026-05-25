# Habit Streak — Test Plan

**Feature:** Habit streak tracking  
**Spec:** `openspec/specs/habit-streak/spec.md`  
**Implementation plan:** `openspec/changes/implementation-plan.md`

## Automated tests

Run from the `habit_tracker` directory:

```powershell
cd habit_tracker
python -m unittest tests.test_streak -v
```

### Covered cases (`tests/test_streak.py`)

| Test | Expected |
|------|----------|
| No completion dates | Streak = 0 |
| Single completion | Streak = 1 |
| Five consecutive calendar days | Streak = 5 |
| Mon–Wed + Fri (gap on Thu) | Streak = 1 |
| Non-contiguous pair vs triple | Streak = 1 or 3 |

## Integration smoke test (Flask test client)

```powershell
cd habit_tracker
python -c "
from datetime import date, timedelta
from app import app, init_db, get_db
import sqlite3

init_db()
client = app.test_client()

# Add habit
client.post('/', data={'name': 'Exercise'}, follow_redirects=True)
habit_id = 1

# Complete 5 consecutive days (backdated for test)
with app.app_context():
    db = get_db()
    for i in range(5):
        d = (date.today() - timedelta(days=4 - i)).isoformat()
        db.execute(
            'INSERT INTO habit_completions (habit_id, completion_date) VALUES (?, ?)',
            (habit_id, d),
        )
    db.commit()

r = client.get('/')
assert b'Streak: 5' in r.data, r.data
print('Integration smoke test: OK')
"
```

## Manual test cases

### TC-1: Mark habit complete

1. Start app: `python app.py`
2. Add habit "Read"
3. Click **Complete today**
4. **Expected:** Button shows **Done today**; streak shows **1**

### TC-2: Five-day streak (acceptance criterion)

Use the integration script above, or complete the same habit on five consecutive real days.

**Expected:** Streak displays **5**.

### TC-3: Missing day resets streak (acceptance criterion)

1. With a 3-day streak (complete 3 days in a row), skip the next calendar day.
2. Complete on the day after the skip.
3. **Expected:** Streak shows **1**, not 4.

### TC-4: Duplicate complete same day

1. Complete a habit today.
2. POST complete again (or refresh and verify button state).
3. **Expected:** Still one completion; streak unchanged; no error.

### TC-5: Delete habit removes streak data

1. Add habit, complete once, note streak = 1.
2. Delete habit.
3. **Expected:** Habit gone; re-adding same name starts streak at 0.

## Pass criteria

- All automated tests pass.
- TC-1, TC-3, and TC-4 pass manually (or via integration script for TC-2).
- UI shows **Streak: N** beside each habit name per spec.
