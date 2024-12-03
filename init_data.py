from datetime import datetime, timedelta
from random import randint
from app.database import SessionLocal, init_db
from app.services.user_service import UserService
from app.services.habit_service import HabitService

# Create 5 sample users with passwords
users_data = [
    {"name": "Alice", "email": "alice@example.com", "password": "Password1@234"},
    {"name": "Bob", "email": "bob@example.com", "password": "paSsword@123"},
    {"name": "Charlie", "email": "charlie@example.com", "password": "$passwOrd123"},
    {"name": "David", "email": "david@example.com", "password": "p*assworD123"},
    {"name": "Eve", "email": "eve@example.com", "password": "(passwoEd123"},
]

# Function to add default users, habits, and tasks
def create_initial_data():
    db = SessionLocal()
    user_service = UserService(db)
    habit_service = HabitService(db)
    
    # Check if there are any users in the database
    users = user_service.get_all_users()
    if users:
        print("Initial data already exists. Skipping creation.")
        return

    for user_data in users_data:
        user = user_service.register(user_data["name"], user_data["email"], user_data["password"])

        # Create habits for each user
        habits_data = [
            {"name": "Exercise", "periodicity": "daily"},
            {"name": "Read a book", "periodicity": "daily"},
            {"name": "Drink water", "periodicity": "daily"},
            {"name": "Go on a date", "periodicity": "weekly"},
            {"name": "Travel", "periodicity": "fortnightly"},
            {"name": "Learn a new language", "periodicity": "weekly"},
            {"name": "Meditation", "periodicity": "daily"},
            {"name": "Cooking", "periodicity": "weekly"},
            {"name": "Clean the house", "periodicity": "monthly"},
        ]

        for habit_data in habits_data:
            # Set habit creation date to exactly 4 weeks ago
            created_at = datetime.now() - timedelta(weeks=4)
            habit = habit_service.create_habit(user, habit_data["name"], habit_data["periodicity"], created_at=created_at, should_add_task=False)

            # Add tasks for each habit based on its periodicity
            tasks_data = generate_task_data(habit_data["periodicity"], created_at)
            for task_data in tasks_data:
                task = habit.add_task(task_data["description"], task_data["start_date"], task_data["end_date"])
                task.completed = task_data["completed"]
                task.completed_at = task_data["completed_at"]
                db.add(task)

    db.commit()
    db.close()
    print("Initial data created successfully!")

def generate_task_data(periodicity: str, created_at: datetime):
    """Generate example task data for the given habit's periodicity, considering the interval from creation to now."""
    tasks_data = []
    now = datetime.now()

    # Calculate number of intervals from created_at to now
    delta = now - created_at
    num_intervals = 0

    if periodicity == "daily":
        num_intervals = delta.days + 1  # Every day is a task, so it's based on the number of days
    elif periodicity == "weekly":
        num_intervals = delta.days // 7 + 1  # Number of weeks from created_at to now
    elif periodicity == "fortnightly":
        num_intervals = delta.days // 14 +1 # Number of 2-week periods from created_at to now
    elif periodicity == "monthly":
        num_intervals = max(1, delta.days // 30) + 1  # Approximate number of months (30 days in a month)
    elif periodicity == "quarterly":
        num_intervals = 1
    elif periodicity == "biannually":
        num_intervals = 1
    elif periodicity == "yearly":
        num_intervals = 1

    # Generate tasks based on the periodicity and the calculated number of intervals
    for interval in range(num_intervals):
        task_start_date = created_at + timedelta(days=interval)
        task_end_date = task_start_date
        completed_at = None
        completed = interval % 2 == 0  # Mark every other task as completed
        if len(tasks_data) > 0:
                # start_date should now be at start of interal
                # last start_date plus 1 day and replace time to 0
                task_start_date = tasks_data[len(tasks_data) - 1]["start_date"] + timedelta(days=1)
                task_start_date = task_start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        if periodicity == "daily":
            task_end_date = task_start_date.replace(hour=23, minute=59, second=59, microsecond=999)
            if completed:
                # choose random hr between 0 to 23
                hr = randint(task_start_date.hour, 23)
                minute = randint(task_start_date.minute, 59)
                second = randint(task_start_date.second, 59)
                completed_at = task_start_date.replace(hour=hr, minute=minute, second=second)
        elif periodicity == "weekly":
            task_end_date = task_start_date.replace(hour=23, minute=59, second=59, microsecond=999) + timedelta(days=6)
            if completed:
                day = randint(0, 6)
                completed_at = task_start_date + timedelta(days=day)
        elif periodicity == "fortnightly":
            task_end_date = task_start_date.replace(hour=23, minute=59, second=59, microsecond=999) + timedelta(days=13)
            if completed:
                day = randint(0, 13)
                completed_at = task_start_date + timedelta(days=day)
        elif periodicity == "monthly":
            next_month = task_start_date.month + 1 if task_start_date.month < 12 else 1
            next_year = task_start_date.year + 1 if task_start_date.month == 12 else task_start_date.year
            task_end_date = task_start_date.replace(day=1, hour=23, minute=59, second=59, microsecond=999, month=next_month, year=next_year) - timedelta(days=1)
        elif periodicity == "quarterly":
            quarter_start_month = ((task_start_date.month - 1) // 3) * 3 + 1
            start_of_quarter = task_start_date.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
            task_end_date = start_of_quarter + timedelta(days=90) - timedelta(seconds=1)
        elif periodicity == "biannually":
            start_of_half_year = task_start_date.replace(month=1 if task_start_date.month <= 6 else 7, day=1, hour=0, minute=0, second=0, microsecond=0)
            task_end_date = start_of_half_year + timedelta(days=181) - timedelta(seconds=1)
        elif periodicity == 'yearly':
            next_year = task_start_date.year + 1
            task_end_date = task_start_date.replace(day=1, month=1, year=next_year, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)

        tasks_data.append({
            "description": f"{periodicity.capitalize()} task {interval + 1}",
            "start_date": task_start_date,
            "end_date": task_end_date,
            "completed": completed_at is not None and completed,
            "completed_at": completed_at,
        })

    return tasks_data

# Run the function to add initial data
if __name__ == "__main__":
    # Initialize the database
    init_db()

    # Create initial data
    create_initial_data()


