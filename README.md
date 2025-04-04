# Habit Tracker
## Overview
This is a **Habit Tracker program** that allows users to manage their daily habits efficiently. Users can create, edit, delete, and track habits while monitoring streaks and progress over time. The application utilizes a CLI (Command Line Interface) for interaction and a database for storage.
## Features
1. **Add a Habit**
Users can add new habits by providing a name, description, and schedule (e.g., daily, weekly).
2. **View All Habits**
Users can view a list of all habits created.
3. **Edit a Habit**
Users can modify existing habits' details.
4. **Delete a Habit**
Specific habits can be removed from the database permanently.
5. **Clear All Habits**
Allows users to delete all habits at once.
6. **Mark Habit as Done**
Users can log events and mark a habit as completed for that day.
7. **Track Streaks**
Tracks current streaks and all-time streaks for each habit to measure consistency.
8. **Filter Habits by Schedule**
Retrieve habits based on their scheduled frequency (e.g., all daily habits).

## Technologies Used
- **Python**: Core language for development.
- **SQLite**: Database to store, retrieve, and manage user data.
- **Command Line Interface**: For user interaction.

## Program Structure
- **main.py**: Entry point of the application. Initializes the database and starts the CLI program.
- **habit.py**: Defines the `Habit` class to represent a habit object. Each habit has attributes like name, description, schedule, and creation date.
- **cli.py**: Contains the `cli` function, which provides the command-line interface for user interaction.
- **manager.py**: Implements a `DataManager` class responsible for managing the application's data logic (e.g., adding, editing, or retrieving habits).
- **habit_controller.py**: Implements a `HabitController` class connecting the CLI and data management layer, encapsulating all major functionality.
- **database.py**: Handles all database operations such as initialization, habit insertion, deletion, updates, etc.
- **test_habit_tracker.py**: Contains unit tests for various features of the program to ensure robustness.

## Installation
1. Clone the repository to your local machine.
2. Ensure you have Python 3.7+ installed.
3. Install required dependencies:
``` bash
   pip install -r requirements.txt
```
1. Run the program:
``` bash
   python main.py
```
## Usage Instructions
1. Upon starting the program, use the CLI options to interact with the system.
2. Available operations include:
    - Adding or editing habits.
    - Viewing all saved habits.
    - Filtering habits by schedule.
    - Tracking progress and streaks.
    - Deleting single habits or clearing all habits.

3. Follow the command prompt for specific instructions.

## Testing the Application
To ensure the application is functioning as expected, you can run unit tests provided in `test_habit_tracker.py`. Execute the following command to run all tests:
``` bash
pytest test_habit_tracker.py
```
## Acknowledgements
This habit tracker was built for personal productivity enthusiasts to help them stay on track and achieve their goals.

