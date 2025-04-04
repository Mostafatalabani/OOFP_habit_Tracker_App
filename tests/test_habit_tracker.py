import sys
import os
import pytest
from datetime import date

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Import modules from your project
from data_manager.manager import DataManager
from models.habit import Habit


# --- Fixtures ---
@pytest.fixture
def manager():
    """
    Fixture to provide a fresh and clean DataManager instance.
    Ensures that tests start with an empty state.
    """
    data_manager = DataManager()
    data_manager.clear_all_habits()
    return data_manager


# --- Tests ---

def test_add_unique_habit(manager):
    """Test adding a unique habit."""
    habit = Habit(name="Exercise", description="Daily workout", schedule="Daily", created_at="")
    manager.add_habit(habit)

    # Check if the habit exists
    habits = manager.get_habits()
    assert len(habits) == 1
    assert habits[0].name == "Exercise"
    assert habits[0].description == "Daily workout"
    assert habits[0].schedule == "Daily"


def test_prevent_duplicate_habits(manager):
    """Test that habits with duplicate names are not allowed."""
    habit1 = Habit(name="Exercise", description="Morning run", schedule="Daily", created_at="")
    manager.add_habit(habit1)

    habit2 = Habit(name="Exercise", description="Evening yoga", schedule="Weekly", created_at="")

    with pytest.raises(ValueError) as exc:
        manager.add_habit(habit2)
    assert "Habit 'Exercise' already exists." in str(exc.value)


def test_prevent_case_insensitive_duplicates(manager):
    """Test that adding habits with duplicate names regardless of case is prevented."""
    habit1 = Habit(name="Exercise", description="Morning run", schedule="Daily", created_at="")
    habit2 = Habit(name="exercise", description="Evening yoga", schedule="Weekly", created_at="")

    manager.add_habit(habit1)
    with pytest.raises(ValueError) as exc:
        manager.add_habit(habit2)
    assert "Habit 'exercise' already exists." in str(exc.value)


def test_view_all_habits(manager):
    """Test retrieving all habits."""
    habit1 = Habit(name="Exercise", description="Daily fitness routine", schedule="Daily", created_at="")
    habit2 = Habit(name="Study", description="Focus on learning new things", schedule="Weekly", created_at="")

    manager.add_habit(habit1)
    manager.add_habit(habit2)

    habits = manager.get_habits()
    assert len(habits) == 2
    names = {habit.name for habit in habits}
    assert "Exercise" in names
    assert "Study" in names


def test_edit_habit(manager):
    """Test editing an existing habit."""
    habit = Habit(name="Exercise", description="Morning workout", schedule="Daily", created_at="")
    manager.add_habit(habit)

    # Edit the habit details
    manager.edit_habit("Exercise", "Morning Exercise", "Updated fitness routine", "Weekly")

    # Verify changes
    habits = manager.get_habits()
    assert len(habits) == 1
    assert habits[0].name == "Morning Exercise"
    assert habits[0].description == "Updated fitness routine"
    assert habits[0].schedule == "Weekly"


def test_delete_habit(manager):
    """Test deleting a habit."""
    habit = Habit(name="Exercise", description="Daily workout", schedule="Daily", created_at="")
    manager.add_habit(habit)

    manager.delete_habit("Exercise")

    # Verify it's deleted
    habits = manager.get_habits()
    assert len(habits) == 0


def test_clear_all_habits(manager):
    """Test clearing all habits."""
    habit1 = Habit(name="Exercise", description="Fitness routine", schedule="Daily", created_at="")
    habit2 = Habit(name="Meditation", description="Relaxation and focus", schedule="Daily", created_at="")
    manager.add_habit(habit1)
    manager.add_habit(habit2)

    # Clear all habits
    manager.clear_all_habits()

    # Validate no habits exist
    habits = manager.get_habits()
    assert len(habits) == 0


def test_mark_habit_as_done(manager):
    """Test marking a habit as done and checking streak correctness."""
    today = date.today().isoformat()
    habit = Habit(name="Exercise", description="Daily workout", schedule="Daily", created_at="")
    manager.add_habit(habit)

    # Mark habit as done
    manager.log_event("Exercise", today)

    # Check streak (assuming a streak of 1 after marking once)
    streak = manager.calculate_streak("Exercise", "daily")
    assert streak == 1

def test_habit_retrieval_by_schedule(manager):
    """Test retrieving habits by their schedule."""
    habit1 = Habit(name="Fitness", description="Morning workout", schedule="Daily", created_at="")
    habit2 = Habit(name="Reading", description="Read a book", schedule="Weekly", created_at="")
    manager.add_habit(habit1)
    manager.add_habit(habit2)

    daily_habits = manager.get_habits_by_schedule("Daily")
    assert len(daily_habits) == 1
    assert daily_habits[0].name == "Fitness"

    weekly_habits = manager.get_habits_by_schedule("Weekly")
    assert len(weekly_habits) == 1
    assert weekly_habits[0].name == "Reading"
