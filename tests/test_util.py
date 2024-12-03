import pytest
from datetime import datetime, timedelta
from app.services.util import compute_start_and_end_date, get_last_interval_for_periodicity

# Test compute_start_and_end_date function
def test_compute_start_and_end_date_daily():
    # Testing daily periodicity
    start_date, end_date = compute_start_and_end_date('daily')
    today = datetime.now().date()
    
    assert start_date.date() == today
    assert end_date.hour == 23
    assert end_date.minute == 59
    assert end_date.second == 59
    assert end_date.microsecond == 999

def test_compute_start_and_end_date_weekly():
    # Testing weekly periodicity
    start_date, end_date = compute_start_and_end_date('weekly')
    today = datetime.now().date()
    expected_end_date = today + timedelta(days=6)
    
    assert start_date.date() == today
    assert end_date.date() == expected_end_date

def test_compute_start_and_end_date_fortnightly():
    # Testing fortnightly periodicity
    start_date, end_date = compute_start_and_end_date('fortnightly')
    today = datetime.now().date()
    expected_end_date = today + timedelta(days=13)
    
    assert start_date.date() == today
    assert end_date.date() == expected_end_date

def test_compute_start_and_end_date_monthly():
    # Testing monthly periodicity
    start_date, end_date = compute_start_and_end_date('monthly')
    today = datetime.now()
    next_month_start = today.replace(day=1) + timedelta(days=32)
    expected_end_date = next_month_start.replace(day=1) - timedelta(days=1)
    
    assert start_date.month == today.month
    assert end_date.date() == expected_end_date.date()

def test_compute_start_and_end_date_quarterly():
    # Testing quarterly periodicity
    start_date, end_date = compute_start_and_end_date('quarterly')
    today = datetime.now()
    quarter_start_month = ((today.month - 1) // 3) * 3 + 1
    expected_end_date = today.replace(month=quarter_start_month, day=1, hour=0, minute=0, second=0, microsecond=0) + timedelta(days=90) - timedelta(seconds=1)

    assert start_date.month == today.month
    assert end_date.date() == expected_end_date.date()

def test_compute_start_and_end_date_biannually():
    # Testing biannually periodicity
    start_date, end_date = compute_start_and_end_date('biannually')
    today = datetime.now()
    half_year_start = today.replace(month=1 if today.month <= 6 else 7, day=1, hour=0, minute=0, second=0, microsecond=0)
    expected_end_date = half_year_start + timedelta(days=181) - timedelta(seconds=1)

    assert start_date.month == today.month
    assert end_date.date() == expected_end_date.date()

def test_compute_start_and_end_date_yearly():
    # Testing yearly periodicity
    start_date, end_date = compute_start_and_end_date('yearly')
    today = datetime.now()
    expected_end_date = today.replace(year=today.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
    
    assert start_date.year == today.year
    assert end_date.date() == expected_end_date.date()

# Test get_last_interval_for_periodicity function
def test_get_last_interval_for_periodicity_daily():
    # Testing the last daily interval
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 1)
    last_start_date, last_end_date = get_last_interval_for_periodicity('daily', start_date, end_date)
    
    expected_last_start_date = start_date - timedelta(days=1)
    expected_last_end_date = end_date - timedelta(days=1)
    
    assert last_start_date == expected_last_start_date
    assert last_end_date == expected_last_end_date

def test_get_last_interval_for_periodicity_weekly():
    # Testing the last weekly interval
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 7)
    last_start_date, last_end_date = get_last_interval_for_periodicity('weekly', start_date, end_date)
    
    expected_last_start_date = start_date - timedelta(weeks=1)
    expected_last_end_date = end_date - timedelta(weeks=1)
    
    assert last_start_date == expected_last_start_date
    assert last_end_date == expected_last_end_date

def test_get_last_interval_for_periodicity_monthly():
    # Testing the last monthly interval
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    last_start_date, last_end_date = get_last_interval_for_periodicity('monthly', start_date, end_date)
    
    expected_last_start_date = start_date - timedelta(days=30)
    expected_last_end_date = end_date - timedelta(days=30)
    
    assert last_start_date == expected_last_start_date
    assert last_end_date == expected_last_end_date

def test_get_last_interval_for_periodicity_yearly():
    # Testing the last yearly interval
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    last_start_date, last_end_date = get_last_interval_for_periodicity('yearly', start_date, end_date)
    
    expected_last_start_date = start_date - timedelta(days=365)
    expected_last_end_date = end_date - timedelta(days=365)
    
    assert last_start_date == expected_last_start_date
    assert last_end_date == expected_last_end_date
