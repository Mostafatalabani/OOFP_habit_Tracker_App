from cli import cli
from db.database import initialize_db

if __name__ == "__main__":
    try:
        # Initialize the database
        initialize_db()
        # Run the CLI program
        cli()
    except Exception as e:
        print(f"Database Initialization Error: {e}")