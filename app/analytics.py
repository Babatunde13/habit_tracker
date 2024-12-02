from app.models import User, Habit, HabitEvent
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

def get_leaderboard(db: Session):
    """Get the leaderboard based on the highest streaks. Returns only top 10 users."""
    leaderboard = []
    users = db.query(User).all()

    for user in users:
        streak = sum(habit.get_streak() for habit in user.habits)
        leaderboard.append((user.name, streak))

    # Sort by streak (highest streak first)
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    # return only top 10 users
    leaderboard = leaderboard[:10]

    return leaderboard

def get_user_longest_streak(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found!")
    
    longest_streak = 0
    habit_with_longest_streak = None
    for habit in user.habits:
        current_streak = habit.get_streaks()
        if current_streak >= longest_streak:
            longest_streak = current_streak
            habit_with_longest_streak = habit
    
    return habit_with_longest_streak, longest_streak

def get_current_habits_for_period(db: Session, user_id: int, period: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found!")
    
    habits = db.query(Habit).filter(Habit.periodicity == period.lower() and Habit.user_id == user.id).all()
    return habits

def get_habits_struggled_most_last_period(db: Session, user_id: int, period: str):
    """Retrieve habits that had the most missed tasks in the last period (daily/weekly/fortnightly/monthly/biannually/yearly)."""
    
    today = datetime.now().date()

    if period == "daily":
        # For daily, we're only interested in today
        start_date = today
        end_date = today

    elif period == "weekly":
        # For weekly, calculate the start of last week (Sunday) and end (next Sunday)
        start_date = today - timedelta(days=today.weekday() + 1)  # Previous Sunday
        end_date = start_date + timedelta(days=6)  # Next Sunday

    elif period == "fortnightly":
        # For fortnightly, calculate the start of the last two weeks (from Sunday)
        start_date = today - timedelta(days=today.weekday() + 1 + 7)  # Previous Sunday, 2 weeks ago
        end_date = start_date + timedelta(days=13)  # End at 14 days later

    elif period == "monthly":
        # For monthly, calculate the start of last month and the end of last month
        first_day_last_month = today.replace(day=1) - timedelta(days=1)  # Last day of previous month
        start_date = first_day_last_month.replace(day=1)  # First day of previous month
        end_date = first_day_last_month  # Last day of the previous month

    elif period == "quarterly":
        # For quarterly, calculate the start of the last quarter
        quarter_start_month = ((today.month - 1) // 3) * 3 + 1
        start_date = today.replace(month=quarter_start_month, day=1)
        end_date = start_date + relativedelta(months=3) - timedelta(days=1)

    elif period == "biannually":
        # For biannually, get the start and end of the last 6 months (two halves of the year)
        if today.month <= 6:
            start_date = today.replace(month=1, day=1)  # First half of the year
            end_date = today.replace(month=6, day=30)  # End of June
        else:
            start_date = today.replace(month=7, day=1)  # Second half of the year
            end_date = today.replace(month=12, day=31)  # End of December

    elif period == "yearly":
        # For yearly, get the first and last day of the previous year
        start_date = today.replace(year=today.year - 1, month=1, day=1)  # Start of last year
        end_date = today.replace(year=today.year - 1, month=12, day=31)  # End of last year

    else:
        raise ValueError("Invalid period. Must be one of: daily, weekly, fortnightly, monthly, biannually, yearly.")

    # Query HabitEvents that fall within the calculated date range for the given period
    missed_tasks_by_habit = (
        db.query(Habit.id, Habit.name, func.count(HabitEvent.id).label('missed_tasks'))
        .join(HabitEvent, HabitEvent.habit_id == Habit.id)
        .filter(Habit.user_id == user_id)
        .filter(HabitEvent.completed == False)  # Only count missed tasks
        .filter(HabitEvent.date >= start_date)
        .filter(HabitEvent.date <= end_date)
        .group_by(Habit.id, Habit.name)
        .order_by(func.count(HabitEvent.id).desc())  # Sort by most missed tasks
        .all()
    )

    # Return habits sorted by the number of missed tasks
    return missed_tasks_by_habit
