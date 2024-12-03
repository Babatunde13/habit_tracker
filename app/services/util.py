from datetime import datetime, timedelta

def compute_start_and_end_date(periodicity: str):
    """
    Compute the start and end date based on the periodicity of the habit.
    If today we start from current time and end at the end of the day.
    If weekly we start from today and end after 6 days.
    If fortnightly we start from today and end after 13 days.
    If monthly we start from beginning of the month and end at the end of the month.
    If quarterly we start from beginning of the quarter and end at the end of the quarter.
    If biannually we start from beginning of the half year and end at the end of the half year.
    If yearly we start from beginning of the year and end at the end of the year.
    """

    today = datetime.now()
    start_date = datetime.now()
    end_date = None
    if periodicity == 'daily':
        end_date = today.replace(hour=23, minute=59, second=59, microsecond=999)
    elif periodicity == 'weekly':
        end_date = today.replace(hour=23, minute=59, second=59, microsecond=999) + timedelta(days=6)
    elif periodicity == 'fortnightly':
        end_date = today.replace(hour=23, minute=59, second=59, microsecond=999) + timedelta(days=13)
    elif periodicity == 'monthly':
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year + 1 if today.month == 12 else today.year
        end_date = today.replace(day=1, hour=23, minute=59, second=59, microsecond=999, month=next_month, year=next_year) - timedelta(days=1)
    elif periodicity == 'quarterly':
        quarter_start_month = ((today.month - 1) // 3) * 3 + 1
        start_of_quarter = today.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = start_of_quarter + timedelta(days=90) - timedelta(seconds=1)
    elif periodicity == 'biannually':
        start_of_half_year = today.replace(month=1 if today.month <= 6 else 7, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = start_of_half_year + timedelta(days=181) - timedelta(seconds=1)
    elif periodicity == 'yearly':
        next_year = today.year + 1
        end_date = today.replace(day=1, month=1, year=next_year, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
    else:
        raise ValueError("Invalid periodicity value")

    return start_date, end_date

def get_last_interval_for_periodicity(periodicity: str, start_date: datetime, end_date: datetime):
    """
    Get the last interval for the given periodicity.
    If weekly, we will get the last week start and end date based on the given start and end date.
    If fortnightly, we will get the last fortnight start and end date based on the given start and end date.
    If monthly, we will get the last month start and end date based on the given start and end date.
    If yearly, we will get the last year start and end date based on the given start and end date.
    """
    days_to_subtract = 0
    if periodicity == "daily":
        days_to_subtract = 1
    elif periodicity == "weekly":
        days_to_subtract = 7
    elif periodicity == "fortnightly":
        days_to_subtract = 14
    elif periodicity == "monthly":
        days_to_subtract = 30
    elif periodicity == "quarterly":
        days_to_subtract = 90
    elif periodicity == "biannually":
        days_to_subtract = 180
    elif periodicity == "yearly":
        days_to_subtract = 365
    else:
        raise ValueError("Invalid periodicity value")
    
    last_start_date = start_date - timedelta(days=days_to_subtract)
    last_end_date = end_date - timedelta(days=days_to_subtract)
    return last_start_date, last_end_date
