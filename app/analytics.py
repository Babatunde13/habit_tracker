from .models import Task, Habit, User
from .services.user_service import UserService
from .services.habit_service import HabitService
from .services.util import compute_start_and_end_date, get_last_interval_for_periodicity
from sqlalchemy.orm import Session
from sqlalchemy import func

def get_leaderboard(db: Session):
    """Get the leaderboard based on the highest streaks. Returns only top 10 users."""
    leaderboard = []
    user_service = UserService(db)
    users = user_service.get_all_users()

    for user in users:
        streak = sum(habit.get_streaks() for habit in user.habits)
        leaderboard.append((user.name, streak))

    # Sort by streak (highest streak first)
    leaderboard.sort(key=lambda x: x[1], reverse=True)

    # return only top 10 users
    leaderboard = leaderboard[:10]

    return leaderboard

def get_user_longest_streak(user: User):
    longest_streak = 0
    habit_with_longest_streak = None
    for habit in user.habits:
        current_streak = habit.get_streaks()
        if current_streak >= longest_streak:
            longest_streak = current_streak
            habit_with_longest_streak = habit
    
    return habit_with_longest_streak, longest_streak

def get_current_habits_for_period(db: Session, user_id: int, period: str):
    """Retrieve habits for the current period (daily/weekly/fortnightly/monthly/biannually/yearly)."""
    habit_service = HabitService(db)
    habits = habit_service.get_user_habits_for_period(user_id, period)
    return habits

def get_habits_struggled_most_last_period(db: Session, user_id: int, period: str):
    """
    Retrieve habits that had the most missed tasks in the last period (daily/weekly/fortnightly/monthly/biannually/yearly).
    """

    # Compute the start and end date for the given period
    start_date, end_date = compute_start_and_end_date(period.lower())
    last_start_date, last_end_date = get_last_interval_for_periodicity(period, start_date, end_date)

    # Query Tasks that fall within the calculated date range for the given period
    missed_tasks_by_habit = (
        db.query(Habit.id, Habit.name, func.count(Task.id).label('missed_tasks'))
        .join(Task, Task.habit_id == Habit.id)
        # Only count missed tasks
        .filter(
            Habit.user_id == user_id, Task.completed == False,
            Task.start_date >= last_start_date, Task.start_date <= last_end_date,
            Task.end_date <= last_end_date, Task.end_date >= last_start_date
        )
        .group_by(Habit.id, Habit.name)
        .order_by(func.count(Task.id).desc())  # Sort by most missed tasks
        .all()
    )

    # Return habits sorted by the number of missed tasks
    return missed_tasks_by_habit
