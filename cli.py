# Author: Mostafa Talabani | Habit Tracker CLI | UID: MT-2025-HT-PRO


import questionary
from controller.habit_controller import HabitController
from datetime import datetime


def cli():
    """
    Command-line interface (CLI) for managing habits, tracking progress,
    and viewing data. This function provides an interactive menu for the
    user to perform various actions related to habit management.

    The CLI is divided into the following sections:
    1. Habit Management: Add, edit, delete, or clear habits.
    2. Tracking Progress: Mark habits as done, view streaks, or show all-time streaks.
    3. Viewing Data: View a detailed list of all habits.
    4. Exit: Exit the application.
    """
    controller = HabitController()  # Initialize the habit controller to handle the logic.

    # Main loop to handle user interactions.
    while True:
        sections = [
            "Habit Management",
            "Tracking Progress",
            "Viewing Data",
            "Exit"
        ]
        # Prompt the user to select a section.
        section_choice = questionary.select("Choose a section:", choices=sections).ask()

        if section_choice == "Habit Management":
            options = [
                "Add Habit",
                "Edit Habit",
                "Delete Habit",
                "Clear All Habits",
                "Back to Main Menu"
            ]
            # Prompt the user to select an option for habit management.
            choice = questionary.select("Choose an option:", choices=options).ask()

            if choice == "Add Habit":
                # Collect details about the new habit to be added.
                name = questionary.text("Enter habit name:").ask()
                description = questionary.text("Enter a description for the habit:").ask()
                schedule = questionary.select(
                    "Set the schedule for the habit:",
                    choices=["daily", "weekly", "monthly"]
                ).ask()
                controller.add_habit(name, description, schedule)  # Add the new habit.

            elif choice == "Edit Habit":
                # Edit an existing habit.
                habits = controller.get_all_habits()
                if not habits:
                    print("No habits available to edit.")  # Inform if no habits exist.
                    continue
                habit_name = questionary.select("Choose a habit to edit:", choices=[h.name for h in habits]).ask()
                new_name = questionary.text("Enter new name (leave blank to keep the same):").ask() or habit_name
                new_description = questionary.text("Enter new description (leave blank to keep the same):").ask()
                new_schedule = questionary.select(
                    "Set the new schedule (leave blank to keep the same):", choices=["daily", "weekly", "monthly"]
                ).ask()
                # Update the selected habit with any new values provided.
                controller.edit_habit(habit_name, new_name, new_description or habits[0].description, new_schedule)

            elif choice == "Delete Habit":
                # Delete a specific habit.
                habits = controller.get_all_habits()
                if not habits:
                    print("No habits available to delete.")  # Inform if no habits exist.
                    continue
                habit_name = questionary.select("Choose a habit to delete:", choices=[h.name for h in habits]).ask()
                controller.delete_habit(habit_name)  # Remove the selected habit.

            elif choice == "Clear All Habits":
                # Clear all existing habits after user confirmation.
                confirm = questionary.confirm("Are you sure you want to delete all habits?").ask()
                if confirm:
                    controller.clear_all_habits()
                    print("All habits cleared.")  # Confirm deletion to the user.

        elif section_choice == "Tracking Progress":
            tracking_options = [
                "Mark Habit as Done",
                "Show Streaks",
                "Show All-Time Streaks",
                "Back to Main Menu"
            ]
            # Prompt the user to select a tracking option.
            tracking_choice = questionary.select("Choose an option:", choices=tracking_options).ask()

            if tracking_choice == "Mark Habit as Done":
                # Mark a habit as completed for the day.
                habits = controller.get_all_habits()
                if not habits:
                    print("No habits available to mark as done.")  # Inform if no habits exist.
                    continue
                habit_name = questionary.select(
                    "Choose a habit you've completed:",
                    choices=[h.name for h in habits]
                ).ask()
                controller.mark_done(habit_name)  # Mark the selected habit as done.

            elif tracking_choice == "Show Streaks":
                # Display streaks for habits based on their schedule.
                streak_type = questionary.select("Choose streak type:", choices=["Daily", "Weekly", "Monthly"]).ask()
                streak_key = streak_type.lower()
                habits = controller.get_habits_by_schedule(streak_key)
                for habit in habits:
                    streak = controller.calculate_streak(habit.name, streak_key)
                    print(f"{habit.name}: {streak} {streak_type.lower()} streak(s) completed.")

            elif tracking_choice == "Show All-Time Streaks":
                # Display all-time streak statistics for all habits.
                habits = controller.get_all_habits()
                for habit in habits:
                    all_time_streak = controller.calculate_all_time_streak(habit.name)
                    print(f"{habit.name}: {all_time_streak} events logged ({habit.schedule}).")

        elif section_choice == "Viewing Data":
            # Display a detailed overview of all habits.
            habits = controller.get_all_habits()
            if not habits:
                print("No habits available.")  # Inform if no habits exist.
                continue
            for habit in habits:
                # Format and display details such as name, description, and creation date.
                created_at = datetime.fromisoformat(habit.created_at).strftime("%Y-%m-%d %H:%M")
                print(f"\nName: {habit.name}")
                print(f"Description: {habit.description}")
                print(f"Schedule: {habit.schedule}")
                print(f"Created At: {created_at}")

        elif section_choice == "Exit":
            # Exit the application gracefully.
            print("Goodbye!")
            break


        elif section_choice == "Exit":
            print("Goodbye!")
            break
