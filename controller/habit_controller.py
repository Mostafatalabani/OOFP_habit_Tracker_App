from data_manager.manager import DataManager
from models.habit import Habit
from datetime import date


class HabitController:
    def __init__(self):
        """
        Controller to manage high-level interactions for habits.
        Uses DataManager for database operations and models Habit instances.
        """
        self.manager = DataManager()

    @staticmethod
    def _sanitize_input(*args):
        """
        Helper method to strip whitespace from provided arguments.

        Args:
            *args: Multiple string arguments to sanitize.

        Returns:
            tuple: Sanitized arguments.
        """
        return (arg.strip() if isinstance(arg, str) else arg for arg in args)

    def add_habit(self, name, description, schedule):
        """
        Add a new habit to the system.

        Args:
            name (str): Name of the habit.
            description (str): Description of the habit.
            schedule (str): Frequency of the habit.
        """
        name, description, schedule = self._sanitize_input(name, description, schedule)
        try:
            habit = Habit(name, description, schedule)
            self.manager.add_habit(habit)
            print(f"Habit '{name}' added successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def edit_habit(self, old_name, new_name, new_description, new_schedule):
        """
        Edit an existing habit's details.

        Args:
            old_name (str): Existing habit name.
            new_name (str): New habit name.
            new_description (str): New description for the habit.
            new_schedule (str): Updated schedule for the habit.
        """
        old_name, new_name, new_description, new_schedule = self._sanitize_input(
            old_name, new_name, new_description, new_schedule
        )
        self.manager.edit_habit(old_name, new_name, new_description, new_schedule)

    def delete_habit(self, name):
        """
        Delete a habit from the system.

        Args:
            name (str): Name of the habit to delete.
        """
        name, = self._sanitize_input(name)
        try:
            self.manager.delete_habit(name)
            print(f"Habit '{name}' deleted successfully!")
        except Exception as e:
            print(f"Error: {e}")

    def clear_all_habits(self):
        """Clear all stored habits."""
        self.manager.clear_all_habits()
        print("All habits cleared successfully!")

    def get_all_habits(self):
        """
        Retrieve all habits from the system.

        Returns:
            list: List of all stored habits.
        """
        try:
            return self.manager.get_habits()
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_habits_by_schedule(self, schedule):
        """
        Retrieve habits by their schedule type.

        Args:
            schedule (str): Frequency to filter the habits, e.g., 'Daily'.

        Returns:
            list: List of habits matching the schedule.
        """
        schedule, = self._sanitize_input(schedule)
        try:
            return self.manager.get_habits_by_schedule(schedule)
        except Exception as e:
            print(f"Error: {e}")
            return []

    def mark_done(self, habit_name):
        """
        Mark a habit as completed for today.

        Args:
            habit_name (str): Name of the habit to mark as done.
        """
        habit_name, = self._sanitize_input(habit_name)
        today = date.today().isoformat()
        try:
            self.manager.log_event(habit_name, today)
            print(f"Habit '{habit_name}' marked as done for today!")
        except Exception as e:
            print(f"Error: {e}")

    def calculate_streak(self, habit_name, streak_type):
        """
        Calculate current streak for a habit.

        Args:
            habit_name (str): Name of the habit.
            streak_type (str): Type of streak ('daily' or 'weekly').

        Returns:
            int: Current streak count.
        """
        habit_name, streak_type = self._sanitize_input(habit_name, streak_type)
        try:
            return self.manager.calculate_streak(habit_name, streak_type)
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def calculate_all_time_streak(self, habit_name):
        """
        Calculate the all-time streak for a habit.

        Args:
            habit_name (str): Name of the habit.

        Returns:
            int: All-time streak count.
        """
        habit_name, = self._sanitize_input(habit_name)
        try:
            return self.manager.calculate_all_time_streak(habit_name)
        except Exception as e:
            print(f"Error: {e}")
            return 0
