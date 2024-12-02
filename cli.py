import click
from app.models import User
from app.services.habit_service import HabitService
from app.services.task_service import TaskService
from app.services.user_service import UserService
from app.database import SessionLocal
from app.analytics import get_leaderboard, get_user_longest_streak, get_current_habits_for_period, get_habits_struggled_most_last_period
from validation import (
    validate_create_habit, validate_register, validate_login,
    validate_update_password, validate_add_task, is_number,
    is_valid_periodicity
)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@click.group("habit-tracker")
def cli():
    """Habit Tracker CLI"""
    pass

def get_user_from_token(db, token: str):
    userService = UserService(db)
    return userService.get_user_from_token(token)

# Command to register a new user
@cli.command("register")
@click.option('--name', prompt='Your name', help='The name of the user.')
@click.option('--email', prompt='Your email', help='The email of the user.')
@click.option('--password', prompt='Your password', hide_input=True, help='The password for the user.')
def register(name: str, email: str, password: str):
    if not validate_register(name, email, password):
        click.echo("Invalid input")

    db = next(get_db())
    user_service = UserService(db)
    
    try:
        user = user_service.register(name, email.lower().strip(), password)
        click.echo(f"User {user.name} registered successfully!")
    except ValueError as e:
        click.echo(f"Error: {e}")
    finally:
        db.close()

# Command to login a user
@cli.command("login")
@click.option('--email', prompt='Your email', help='The email of the user.')
@click.option('--password', prompt='Your password', hide_input=True, help='The password of the user.')
def login(email: str, password: str):
    if not validate_login(email, password):
        click.echo("Invalid input")

    db = next(get_db())
    user_service = UserService(db)
    
    user = user_service.login(email.lower().strip(), password)
    if user:
        click.echo(f"Login successful! Welcome back, {user.name}.")
        click.echo(f"Your email is: {user.email}")
        token = user_service.get_auth_token(user.email)
        click.echo(f"Your token is: {token}")
    else:
        click.echo("Invalid credentials. Please try again.")
    db.close()

# Command to update user password
@cli.command("update-password")
@click.option('--email', prompt='Your email', help='The email of the user.')
@click.option('--old_password', prompt='Old password', hide_input=True, help='The current password of the user.')
@click.option('--new_password', prompt='New password', hide_input=True, help='The new password for the user.')
def update_password(email: str, old_password: str, new_password: str):
    if not validate_update_password(email, old_password, new_password):
        click.echo("Invalid input")

    db = next(get_db())
    user_service = UserService(db)

    try:
        user = user_service.update_password(email.lower().strip(), old_password, new_password)
        click.echo(f"Password updated successfully for user {user.name}.")
    except ValueError as e:
        click.echo(f"Error: {e}")
    db.close()

# Command to create a new habit
@cli.command("create-habit")
@click.option('--token', prompt='Token', help='The auth token of the user.')
@click.option('--name', prompt='Habit name', help='The name of the habit.')
@click.option('--periodicity', prompt='Periodicity', help='The periodicity of the habit (daily, weekly).')
def create_habit(token: str, name: str, periodicity: str):
    if not validate_create_habit(name, periodicity):
        click.echo("Invalid Input")

    db = next(get_db())
    habit_service = HabitService(db)
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    habit = habit_service.create_habit(user=user, name=name, periodicity=periodicity.lower())
    print("Habit is almos tdone")
    db.add(habit)
    db.commit()
    click.echo(f"Habit {name} created for user {user.name}.")
    db.close()

# Command to list available habits
@cli.command("list-habits")
@click.option('--token', prompt='Token', help='The auth token of the user.')
def list_habits(token: str):
    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    habit_service = HabitService(db)
    habits = habit_service.get_all_habits(user)
    click.echo(f"Habits for user {user.name}:")
    for habit in habits:
        click.echo(f"{habit.id}. {habit.name} ({habit.periodicity})")
    db.close()

# Command to add a task to a habit
@cli.command("add-task")
@click.option('--token', prompt='Token', help='The auth token of the user.')
@click.option('--habit_id', prompt='Habit ID', help='The ID of the habit.', type=int)
@click.option('--description', prompt='Task description', help='Description of the task.')
def add_task(token: str, habit_id: int, description: str):
    if  not validate_add_task(habit_id, description):
        click.echo("Invalid input")

    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    habit_service = HabitService(db)
    habit = habit_service.get_habit(user.id, habit_id)
    if not habit:
        click.echo("Habit not found!")
        return
    task_service = TaskService(db)
    task = task_service.create_task(habit, description)
    db.add(task)
    db.commit()
    click.echo(f"Task '{description}' added to habit {habit.name}.")
    db.close()

# Command to list tasks for a habit
@cli.command("list-tasks")
@click.option('--token', prompt='Token', help='The auth token of the user.')
@click.option('--habit_id', prompt='Habit ID', help='The ID of the habit.', type=int)
def list_tasks(token: str, habit_id: int):
    if not is_number(habit_id):
        click.echo("Habit ID must be an number!")
        click.echo("Invalid input")

    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    habit_service = HabitService(db)
    habit = habit_service.get_habit(user.id, habit_id)
    if not habit:
        click.echo("Habit not found!")
        return

    tasks = habit.get_tasks()
    if len(tasks) == 0:
        click.echo(f"No tasks found for habit {habit.name}.")
    else:
        click.echo(f"Tasks for habit {habit.name}:")
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            click.echo(f"{task.id}. {task.description} - {status}")
    db.close()

# Command to mark a task as completed
@cli.command("complete-task")
@click.option('--token', prompt='Token', help='The auth token of the user.')
@click.option('--task_id', prompt='Task ID', help='The ID of the task.', type=int)
def complete_task(token: str, task_id: int):
    if not is_number(task_id):
        click.echo("Task ID must be an number!")
        click.echo("Invalid input")

    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    task_service = TaskService(db)
    try:
        task = task_service.complete_task(user.id, task_id)
        db.commit()
        click.echo(f"Task {task.description} marked as completed.")
    except ValueError as e:
        click.echo(f"Error: {e}")
        db.rollback()
    
    db.close()

# Command to mark a task as uncompleted
@cli.command("uncomplete-task")
@click.option('--token', prompt='Token', help='The auth token of the user.')
@click.option('--task_id', prompt='Task ID', help='The ID of the task.', type=int)
def uncomplete_task(token: str, task_id: int):
    if not is_number(task_id):
        click.echo("Task ID must be an number!")
        click.echo("Invalid input")

    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    task_service = TaskService(db)
    task = task_service.uncomplete_task(user.id, task_id)
    db.commit()
    click.echo(f"Task {task.description} marked as uncompleted.")
    db.close()

# Command to show analytics
@cli.command("show-current-streaks")
@click.option('--token', prompt='Token', help='The auth token of the user.')
def show_current_streaks(token: str):
    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    habit_service = HabitService(db)
    user = db.query(User).filter(User.id == user.id).first()
    if not user:
        click.echo("User not found!")
        return

    habits = user.habits
    for habit in habits:
        streak = habit_service.get_streak(habit)
        is_day = "day" if streak == 1 or streak == 0 else "days"
        click.echo(f"User {user.name} has habit {habit.name} with a current streak of {streak} {is_day}.")
    db.close()

# Command to show the user's longest streak
@cli.command("longest-streak")
@click.option('--token', prompt='Token', help='The auth token of the user.')
def longest_streak(token: str):
    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    habit, streak = get_user_longest_streak(db, user.id)
    if not habit:
        click.echo("No habits found for the user.")
        return

    click.echo(f"User {user.name} has the longest streak of {streak} days for habit {habit.name}.")
    db.close()

# Command to show the current habits for a period
@cli.command("current-habits")
@click.option('--token', prompt='Token', help='The auth token of the user.')
@click.option('--period', prompt='Period', help='The period to check habits for (daily, weekly, etc.).')
def current_habits(token: str, period: str):
    if not is_valid_periodicity(period):
        click.echo("Invalid period. Please provide a valid period (daily, weekly, forthnightly, monthly, quarterly, bianually, yearly)")
        return
    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    habits = get_current_habits_for_period(db, user.id, period.lower())
    if not habits:
        click.echo(f"No habits found for the user for the period {period}.")
        return

    click.echo(f"Current habits for user {user.name} for period {period}:")
    for habit in habits:
        click.echo(f"{habit.id}. {habit.name}")
    db.close()

# Command to show the habits struggled most in the last period
@cli.command("struggled-habits")
@click.option('--token', prompt='Token', help='The auth token of the user.')
@click.option('--period', prompt='Period', help='The period to check habits for (daily, weekly, etc.).')
def struggled_habits(token: str, period: str):
    if not is_valid_periodicity(period):
        click.echo("Invalid period. Please provide a valid period (daily, weekly, forthnightly, monthly, quarterly, bianually, yearly)")
        return

    db = next(get_db())
    user = get_user_from_token(db, token)
    if not user:
        click.echo("User not found!")
        return

    habits = get_habits_struggled_most_last_period(db, user.id, period)
    if not habits:
        click.echo(f"No struggled habits found for the period {period}.")
        return

    click.echo(f"Habits struggled most in the last period ({period}):")
    for habit in habits:
        click.echo(f"{habit.name}")
    db.close()

# Command to show the leaderboard
@cli.command("leaderboard")
def leaderboard():
    db = next(get_db())
    leaderboard = get_leaderboard(db)
    click.echo("Leaderboard (Top Streaks):")
    for rank, (user_name, streak) in enumerate(leaderboard, 1):
        click.echo(f"{rank}. {user_name} - Streak: {streak} days")

    db.close()

if __name__ == "__main__":
    cli()
