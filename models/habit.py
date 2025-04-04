class Habit:
    def __init__(self, name: str, description: str, schedule: str, created_at: str = ""):
        """
        Represents a Habit instance with basic details.

        Args:
            name (str): Name of the habit.
            description (str): Description of the habit.
            schedule (str): Habit schedule (e.g., daily, weekly).
            created_at (str): Creation date of the habit.
        """
        self.name = name.strip()  # Normalize name
        self.description = description.strip()  # Normalize description
        self.schedule = schedule.strip()  # Normalize schedule
        self.created_at = created_at.strip() if created_at else ""  # Normalize created_at
