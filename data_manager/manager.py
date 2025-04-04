from db.database import (
    get_db,
    insert_habit,
    edit_habit,
    delete_habit,
    clear_all_habits,
    fetch_habits,
    fetch_habits_by_schedule,
    log_event,
    count_habit_events,
    count_all_time_streak,
)
from models.habit import Habit


class DataManager:
    """
    Handles database interactions related to habits:
    Adding, editing, deleting, fetching, and other data manipulations.
    """

    def __init__(self, db=None):
        """
        Initializes the DataManager with a database connection.

        :param db: Optional database connection object. If not provided, the default database is used.
        """
        self.db = db if db else get_db()

    def add_habit(self, habit: Habit):
        """
        Adds a new habit to the database.

        :param habit: An instance of the Habit class representing the habit.
        :raises ValueError: If the habit name is empty or a duplicate already exists.
        """
        if not habit.name.strip():
            raise ValueError("Habit name cannot be empty.")

        # Check for duplicates in the database
        existing_habits = fetch_habits(self.db)
        normalized_name = habit.name.strip().lower()
        if any(h[0].strip().lower() == normalized_name for h in existing_habits):
            raise ValueError(f"Habit '{habit.name}' already exists.")

        # Insert the habit into the database
        insert_habit(self.db, habit.name.strip(), habit.description.strip(), habit.schedule.strip())

    def edit_habit(self, old_name, new_name, new_description, new_schedule):
        """
        Updates an existing habit in the database.

        :param old_name: Current name of the habit to be edited.
        :param new_name: Updated name for the habit.
        :param new_description: Updated description for the habit.
        :param new_schedule: Updated schedule for the habit.
        """
        edit_habit(self.db, old_name.strip(), new_name.strip(), new_description.strip(), new_schedule.strip())

    def delete_habit(self, name):
        """
        Deletes a habit from the database.

        :param name: Name of the habit to be deleted.
        """
        delete_habit(self.db, name.strip())

    def clear_all_habits(self):
        """
        Removes all habits from the database.
        """
        clear_all_habits(self.db)

    def get_habits(self):
        """
        Retrieves all habits from the database.

        :return: A list of Habit objects representing all habits in the database.
        """
        rows = fetch_habits(self.db)
        return [Habit(*row) for row in rows]

    def get_habits_by_schedule(self, schedule):
        """
        Retrieves habits based on their schedule (e.g., daily, weekly).

        :param schedule: The schedule type to filter habits by (e.g., "daily").
        :return: A list of Habit objects filtered by the given schedule.
        """
        rows = fetch_habits_by_schedule(self.db, schedule.strip())
        return [Habit(*row) for row in rows]

    def log_event(self, habit_name, event_date):
        """
        Logs a habit completion event.

        :param habit_name: Name of the habit to log the event for.
        :param event_date: The date the event occurred (ISO format).
        """
        log_event(self.db, habit_name.strip(), event_date)

    def calculate_streak(self, habit_name, streak_type):
        """
        Calculates the current streak for a habit based on the streak type.

        :param habit_name: Name of the habit.
        :param streak_type: Type of streak to calculate (e.g., "daily").
        :return: The current streak count.
        """
        return count_habit_events(self.db, habit_name.strip(), streak_type)

    def calculate_all_time_streak(self, habit_name):
        """
        Calculates the all-time longest streak for a habit.

        :param habit_name: Name of the habit.
        :return: The longest streak count.
        """
        return count_all_time_streak(self.db, habit_name.strip())
