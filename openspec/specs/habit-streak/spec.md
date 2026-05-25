# Habit Streak Tracking Feature Specification

## Overview

This specification defines the Habit Streak Tracking feature for the Habit Tracker application.

The feature helps users maintain consistency by tracking the number of consecutive days they complete a habit.

---

## Problem Statement

Users currently can create and manage habits, but there is no mechanism to motivate long-term consistency.

A streak system encourages users to complete habits regularly by showing consecutive completion days.

---

## Objective

Implement a streak tracking feature that:

- Tracks consecutive completion days for each habit
- Displays the current streak count
- Resets the streak when a day is missed
- Updates streak information automatically

---

## User Story

As a user,

I want to see how many consecutive days I have completed a habit,

So that I stay motivated and maintain consistency.

---

## Functional Requirements

### FR-1: Habit Completion

The user shall be able to mark a habit as completed for the current day.

### FR-2: Store Completion History

The system shall store completion dates for each habit.

### FR-3: Streak Calculation

The system shall calculate consecutive completion days.

### FR-4: Streak Display

The current streak count shall be displayed next to each habit.

### FR-5: Streak Reset

The streak shall reset when a habit is not completed for a required day.

---

## Non-Functional Requirements

### NFR-1

The streak calculation should execute quickly.

### NFR-2

The implementation should be modular and maintainable.

### NFR-3

The feature should integrate with the existing Habit Tracker application.

---

## Acceptance Criteria

### AC-1

Given a user completes a habit for 3 consecutive days,

When the streak is calculated,

Then the streak value should be 3.

### AC-2

Given a user misses a day,

When the streak is recalculated,

Then the streak should reset.

### AC-3

Given a habit exists,

When the habit list is displayed,

Then the current streak count should be visible.

### AC-4

The application should continue functioning normally after adding the streak feature.

---

## Technical Design

### New Module

Create:

```text
streak.py
```

### Responsibilities

- Calculate current streak
- Validate completion dates
- Reset streak when required

### Tests

Create:

```text
tests/test_streak.py
```

to verify:

- Consecutive streak calculation
- Streak reset behavior
- Edge cases

---

## Deliverables

- streak.py
- tests/test_streak.py
- Updated Habit Tracker integration
- Passing test cases
