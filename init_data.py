from app.database import SessionLocal, init_db
from app.models import User, Habit, Task, HabitEvent
from datetime import datetime

# Initialize the database
init_db()

# Function to add default users, habits, and tasks
def create_initial_data():
    db = SessionLocal()
    # check if there are any users in the database
    users = db.query(User).all()
    if users:
        print("Initial data already exists. Skipping creation.")
        return

    # Create 5 sample users with passwords
    users_data = [
        {"name": "Alice", "email": "alice@example.com", "password": "password1234"},
        {"name": "Bob", "email": "bob@example.com", "password": "password@123"},
        {"name": "Charlie", "email": "charlie@example.com", "password": "$password123"},
        {"name": "David", "email": "david@example.com", "password": "p*assword123"},
        {"name": "Eve", "email": "eve@example.com", "password": "(password123"},
    ]

    for user_data in users_data:
        user = User(name=user_data["name"], email=user_data["email"])
        user.set_password(user_data["password"])  # Set password as hashed
        db.add(user)

        # Create habits for each user
        habits_data = [
            {"name": "Exercise", "periodicity": "weekly"},
            {"name": "Read a book", "periodicity": "daily"},
            {"name": "Drink water", "periodicity": "daily"},
            {"name": "Go on a date", "periodicity": "monthly"},
            {"name": "Travel", "periodicity": "bianually"},
        ]

        for habit_data in habits_data:
            habit = Habit(name=habit_data["name"], periodicity=habit_data["periodicity"], user=user)
            db.add(habit)

            # Add sample tasks for each habit
            tasks_data = [
                {"description": f"{habit.name} task 1", "completed": False},
                {"description": f"{habit.name} task 2", "completed": True}
            ]

            for task_data in tasks_data:
                task = Task(description=task_data["description"], completed=task_data["completed"], habit=habit)
                db.add(task)
                if task_data["completed"]:
                    event = HabitEvent(habit=habit, completed=task_data["completed"], date=datetime.now())
                    db.add(event)

    db.commit()
    db.close()
    print("Initial data created successfully!")

# Run the function to add initial data
if __name__ == "__main__":
    create_initial_data()
