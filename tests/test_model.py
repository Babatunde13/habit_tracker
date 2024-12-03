import pytest
from app.models import User, Task, Habit
from datetime import datetime, timedelta

def test_set_password(sample_user):
    """Test that the password is hashed and stored."""
    assert sample_user.check_password("pasSword@123")
    assert not sample_user.check_password("wrongpassword")


def test_create_user(db_session):
    """Test that a user is created successfully."""
    user = User(name="New User", email="newuser@example.com")
    user.set_password("newpassword123")
    db_session.add(user)
    db_session.commit()
    
    fetched_user = db_session.query(User).filter(User.email == "newuser@example.com").first()
    assert fetched_user is not None
    assert fetched_user.name == "New User"


def test_user_password_check_invalid(sample_user):
    """Test that password verification fails with the wrong password."""
    assert not sample_user.check_password("wrongpassword")

def test_create_habit(db_session, sample_user):
    """Test that a habit can be created for a user."""
    habit = Habit(name="Read a book", periodicity="daily", user=sample_user)
    db_session.add(habit)
    db_session.commit()

    fetched_habit = db_session.query(Habit).filter(Habit.name == "Read a book").first()
    assert fetched_habit is not None
    assert fetched_habit.user_id == sample_user.id


def test_streak_calculation(db_session, sample_user, sample_habit):
    """Test that the streak is correctly calculated for the habit."""
    task1 = Task(description="Task 1", habit=sample_habit, completed=True, start_date=datetime.now())
    task2 = Task(description="Task 2", habit=sample_habit, completed=True, start_date=datetime.now())
    end_date = datetime.now() + timedelta(days=1)
    task1.end_date = end_date
    task2.end_date = end_date
    db_session.add(task1)
    db_session.add(task2)
    db_session.commit()

    streak = sample_habit.get_current_streaks()
    assert streak == 2


def test_longest_streak_calculation(db_session, sample_user, sample_habit):
    """Test that the longest streak is calculated correctly."""
    task1 = Task(description="Task 1", habit=sample_habit, completed=True, start_date=datetime.now())
    task2 = Task(description="Task 2", habit=sample_habit, completed=False, start_date=datetime.now())
    task3 = Task(description="Task 3", habit=sample_habit, completed=True, start_date=datetime.now())
    end_date = datetime.now() + timedelta(days=1)
    task2.end_date = end_date
    task1.end_date = end_date
    task3.end_date = end_date
    db_session.add(task1)
    db_session.add(task2)
    db_session.add(task3)
    db_session.commit()

    longest_streak = sample_habit.get_longest_streaks()
    assert longest_streak == 1

def test_complete_task(db_session, sample_task):
    """Test that a task can be marked as completed."""
    assert sample_task.completed is False
    
    sample_task.complete()
    
    assert sample_task.completed is True
    assert sample_task.completed_at is not None


def test_complete_task_overdue(db_session, sample_task):
    """Test that a task cannot be completed if it's overdue."""
    sample_task.end_date = datetime.now() - timedelta(days=1)  # Set end date to the past
    with pytest.raises(ValueError, match="Task is overdue and cannot be completed."):
        sample_task.complete()

