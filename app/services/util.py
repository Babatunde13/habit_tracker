from app.models import Habit, HabitEvent
from datetime import datetime, timedelta

def is_in_range(habit: Habit, event: HabitEvent):
    """
    Check if the habit event was completed within the given range based on habit periodicity.
    """
    today = datetime.now().date()
    created_at = event.created_at.date()
    periodicity = habit.periodicity

    # Handle 'daily' periodicity
    if periodicity == "daily":
        return created_at == today

    # Handle 'weekly' periodicity
    elif periodicity == "weekly":
        # Get the start of the week for both today and the created_at date (Sunday to Saturday)
        start_of_week_today = today - timedelta(days=today.weekday())  # Start of this week (Sunday)
        end_of_week_today = start_of_week_today + timedelta(days=6)  # End of this week (Saturday)
        
        start_of_week_created = created_at - timedelta(days=created_at.weekday())  # Start of the week for created_at
        end_of_week_created = start_of_week_created + timedelta(days=6)  # End of the week for created_at

        return start_of_week_today == start_of_week_created and end_of_week_today == end_of_week_created

    # Handle 'fortnightly' periodicity (every two weeks)
    elif periodicity == "fortnightly":
        # Calculate the start of the two-week period (from Sunday to Sunday)
        start_of_fortnight_today = today - timedelta(days=today.weekday() + 1 + 7)  # Start of last fortnight (two Sundays ago)\
        end_of_fortnight = start_of_fortnight_today + timedelta(days=13)  # 13 days after the start of the fortnight

        start_of_fortnight_created = created_at - timedelta(days=created_at.weekday() + 1)  # Start of the fortnight for created_at
        end_of_fortnight_created = start_of_fortnight_created + timedelta(days=13)  # 13 days after the start of the fortnight
        return start_of_fortnight_today == start_of_fortnight_created and end_of_fortnight == end_of_fortnight_created

    # Handle 'monthly' periodicity
    elif periodicity == "monthly":
        # Compare the month and year
        return today.year == created_at.year and today.month == created_at.month

    # Handle 'quarterly' periodicity (every 3 months)
    elif periodicity == "quarterly":
        # Calculate the quarter of the year (1-4)
        quarter_today = (today.month - 1) // 3 + 1
        quarter_created = (created_at.month - 1) // 3 + 1
        return today.year == created_at.year and quarter_today == quarter_created

    # Handle 'biannually' periodicity (every 6 months)
    elif periodicity == "biannually":
        # Compare if the habit was created in the same half of the year
        half_of_year_today = 1 if today.month <= 6 else 2
        half_of_year_created = 1 if created_at.month <= 6 else 2
        return today.year == created_at.year and half_of_year_today == half_of_year_created

    # Handle 'yearly' periodicity
    elif periodicity == "yearly":
        # Compare if the habit was created in the same year
        return today.year == created_at.year

    # If the periodicity doesn't match any of the expected values, return False
    return False
