import sqlite3
from datetime import datetime


def get_db(db_name="habits.db"):
    """
    Connect to the database.
    """
    return sqlite3.connect(db_name)


def initialize_db():
    """
    Initialize the required database tables.
    """
    conn = get_db()
    cursor = conn.cursor()

    # Create the habits table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            schedule TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)

    # Create the habit events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (habit_name) REFERENCES habits (name)
        );
    """)

    conn.commit()
    conn.close()


def insert_habit(db, name, description, schedule):
    """
    Insert a new habit into the habits table.
    """
    cursor = db.cursor()
    created_at = datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO habits (name, description, schedule, created_at) VALUES (?, ?, ?, ?)",
            (name, description, schedule, created_at)
        )
    except sqlite3.IntegrityError:
        print(f"Error: The habit '{name}' already exists!")
    db.commit()


def edit_habit(db, old_name, new_name, new_description, new_schedule):
    """
    Edit an existing habit's name, description, and schedule.
    """
    cursor = db.cursor()
    cursor.execute("""
        UPDATE habits
        SET name = ?, description = ?, schedule = ?
        WHERE name = ?
    """, (new_name, new_description, new_schedule, old_name))
    db.commit()


def delete_habit(db, name):
    """
    Delete a specific habit.
    """
    cursor = db.cursor()
    cursor.execute("DELETE FROM habits WHERE name = ?", (name,))
    cursor.execute("DELETE FROM habit_events WHERE habit_name = ?", (name,))
    db.commit()


def clear_all_habits(db):
    """
    Delete all habits and their associated events from the database.
    """
    cursor = db.cursor()
    cursor.execute("DELETE FROM habits")
    cursor.execute("DELETE FROM habit_events")
    db.commit()


def fetch_habits(db):
    """
    Get all habits from the database.
    """
    cursor = db.cursor()
    cursor.execute("SELECT name, description, schedule, created_at FROM habits")
    return cursor.fetchall()


def fetch_habits_by_schedule(db, schedule):
    """
    Get habits filtered by their schedule (daily, weekly, or monthly).
    """
    cursor = db.cursor()
    cursor.execute("SELECT name, description, schedule, created_at FROM habits WHERE schedule = ?", (schedule,))
    return cursor.fetchall()


def log_event(db, habit_name, date):
    """
    Log a habit completion event.
    """
    cursor = db.cursor()
    cursor.execute("INSERT INTO habit_events (habit_name, date) VALUES (?, ?)", (habit_name, date))
    db.commit()


def count_habit_events(db, habit_name, streak_type):
    """
    Count habit events for streaks (daily, weekly, monthly).
    """
    cursor = db.cursor()

    if streak_type == "daily":
        cursor.execute("""
            SELECT COUNT(*) FROM habit_events 
            WHERE habit_name = ? AND date = DATE('now');
        """, (habit_name,))
    elif streak_type == "weekly":
        cursor.execute("""
            SELECT COUNT(*) FROM habit_events 
            WHERE habit_name = ? AND date >= DATE('now', '-7 days');
        """, (habit_name,))
    elif streak_type == "monthly":
        cursor.execute("""
            SELECT COUNT(*) FROM habit_events 
            WHERE habit_name = ? AND date >= DATE('now', '-30 days');
        """, (habit_name,))

    result = cursor.fetchone()
    return result[0] if result else 0


def count_all_time_streak(db, habit_name):
    """
    Count the total number of logged events for a habit (all-time streak).
    """
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM habit_events WHERE habit_name = ?;
    """, (habit_name,))
    result = cursor.fetchone()
    return result[0] if result else 0
