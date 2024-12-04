import pytest
from datetime import timedelta
from click.testing import CliRunner
from client import cli
from app.services.user_service import UserService
from app.services.habit_service import HabitService
from app.services.task_service import TaskService

@pytest.fixture
def runner():
    """Create a runner to test CLI commands."""
    return CliRunner()


# Test for user registration
def test_register(runner, db_session):
    """Test the register CLI command"""
    # Simulate user input
    result = runner.invoke(cli, ['register', '--name', 'Alice', '--email', 'alice@example.com', '--password', 'passS#ord123'])
    
    # Check if the registration was successful
    assert result.exit_code == 0
    assert "User Alice registered successfully!" in result.output
    
    # Verify that the user was actually added to the database
    user_service = UserService(db_session)
    user = user_service.get_user('alice@example.com')
    assert user is not None
    assert user.name == 'Alice'


# Test for user login
def test_login(runner, db_session):
    """Test the login CLI command"""
    # First, create a user for login
    user_service = UserService(db_session)
    user_service.register(name="Bob", email="bob1@example.com", password="paAsword@123", should_commit=True)

    # Simulate login command
    result = runner.invoke(cli, ['login', '--email', 'bob1@example.com', '--password', 'paAsword@123'])

    # Check if login was successful
    assert result.exit_code == 0
    assert "Login successful! Welcome back, Bob." in result.output
    assert "Your email is: bob1@example.com" in result.output
    assert "Your token is: " in result.output

    # test invalid login
    result = runner.invoke(cli, ['login', '--email', 'bob1@example.com', '--password', 'wR#on12gpassword'])
    assert "Invalid credentials" in result.output


# Test for habit creation
def test_create_habit(runner, db_session):
    """Test the create-habit CLI command"""
    # First, create a user
    user_service = UserService(db_session)
    user = user_service.register(name="Charlie", email="charlie@example.com", password="passS#ord123", should_commit=True)

    # Generate an authentication token for the user
    token = user_service.get_auth_token(user.email)

    # Simulate creating a habit for the user
    result = runner.invoke(cli, ['create-habit', '--token', token, '--name', 'Exercise', '--periodicity', 'daily'])

    # Check if the habit was successfully created
    assert result.exit_code == 0
    assert "Habit Exercise created for user Charlie." in result.output
    assert "A new task has been created for the habit" in result.output


# Test for listing habits
def test_list_habits(runner, db_session):
    """Test the list-habits CLI command"""
    # Create a user and habit
    user_service = UserService(db_session)
    user = user_service.register(name="David", email="david1234@example.com", password="passS#ord123", should_commit=True)
    habit_service = HabitService(db_session)
    habit = habit_service.create_habit(user=user, name="Read a book", periodicity="daily", should_add_task=True)
    
    # Generate an authentication token for the user
    token = user_service.get_auth_token(user.email)

    # Simulate listing habits
    result = runner.invoke(cli, ['list-habits', '--token', token])
    tasks = habit.tasks

    # Check if the habit is listed correctly
    assert result.exit_code == 0
    assert "Habits for user David:" in result.output
    assert f"{habit.id}. Read a book (daily)" in result.output


# Test for updating password
def test_update_password(runner, db_session):
    """Test the update-password CLI command"""
    # Create a user
    user_service = UserService(db_session)
    user = user_service.register(name="Eve", email="eve12@example.com", password="passS#ord123", should_commit=True)

    # Simulate updating password
    result = runner.invoke(cli, ['update-password', '--email', 'eve12@example.com', '--old_password', 'passS#ord123', '--new_password', 'newpSssS#ord123'])

    # Check if the password was updated
    assert result.exit_code == 0
    assert "Password updated successfully for user Eve." in result.output

    # Verify password update
    updated_user = user_service.get_user('eve12@example.com')
    assert updated_user.check_password('newpSssS#ord123')


# Test for leaderboard display
def test_leaderboard(runner, db_session):
    """Test the leaderboard CLI command"""
    # Create some users and habits for testing
    user_service = UserService(db_session)
    user1 = user_service.register(name="Frank", email="frank@example.com", password="passS#ord123", should_commit=True)
    user2 = user_service.register(name="Grace", email="grace@example.com", password="passS#ord123", should_commit=True)
    
    habit_service = HabitService(db_session)
    habit1 = habit_service.create_habit(user=user1, name="Jogging", periodicity="daily", should_add_task=True)
    habit2 = habit_service.create_habit(user=user2, name="Yoga", periodicity="daily", should_add_task=True)

    # Simulate the leaderboard command
    result = runner.invoke(cli, ['leaderboard'])

    # Check if leaderboard displays the users
    assert result.exit_code == 0
    assert "Leaderboard (Top Streaks):" in result.output
    assert "Frank" in result.output
    assert "Grace" in result.output

# Test for updating habit
def test_update_habit(runner, db_session):
    user_service = UserService(db_session)
    user = user_service.register(name="Alice", email="alice12344@example.com", password="P@assword123", should_commit=True)

    habit_service = HabitService(db_session)
    habit = habit_service.create_habit(user=user, name="Exercise", periodicity="daily", should_add_task=True)

    old_name = habit.name
    new_name = "Morning Exercise"

    # Run the update_habit command
    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['update-habit', '--token', token, '--habit_id', habit.id, '--name', new_name])
    assert result.exit_code == 0
    assert f'Habit "{old_name}" changed to "{new_name}".' in result.output


# Test for listing tasks
def test_list_tasks(runner, db_session):
    user_service = UserService(db_session)
    user = user_service.register(name="Bob", email="bob@example.com", password="P@assword123", should_commit=True)

    habit_service = HabitService(db_session)
    habit = habit_service.create_habit(user=user, name="Read", periodicity="daily", should_add_task=True)

    task_service = TaskService(db_session)
    task = habit.tasks[0]
    task_service.complete_task(user.id, task.id)

    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['list-tasks', '--token', token, '--habit_id', habit.id])
    assert result.exit_code == 0
    assert f"{task.id}. Read task 1 - Completed" in result.output 


# Test for completing a task
def test_complete_task(runner, db_session):
    user_service = UserService(db_session)
    user = user_service.register(name="Charlie", email="charlie1@example.com", password="P@assword123", should_commit=True)

    habit_service = HabitService(db_session)
    habit = habit_service.create_habit(user=user, name="Jogging", periodicity="daily", should_add_task=True)
    task = habit.tasks[0]

    # Run complete_task command
    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['complete-task', '--token', token, '--task_id', task.id])
    assert result.exit_code == 0
    assert "Task Jogging task 1 marked as completed." in result.output


# Test for showing current streaks
def test_show_current_streaks(runner, db_session):
    user_service = UserService(db_session)
    user = user_service.register(name="Eve", email="eve@example.com", password="P@assword123", should_commit=True)

    habit_service = HabitService(db_session)
    habit = habit_service.create_habit(user=user, name="Exercise", periodicity="daily", should_add_task=True)

    task_service = TaskService(db_session)
    task = habit.tasks[0]
    task_service.complete_task(user.id, task.id)

    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['show-current-streaks', '--token', token])
    assert result.exit_code == 0
    assert "User Eve has habit Exercise with a current streak of 1 day" in result.output


# Test for longest streak
def test_longest_streak(runner, db_session):
    user_service = UserService(db_session)
    user = user_service.register(name="David", email="david@example.com", password="Passwor#d123", should_commit=True)

    habit_service = HabitService(db_session)
    habit = habit_service.create_habit(user=user, name="Jogging", periodicity="daily", should_add_task=True)

    task_service = TaskService(db_session)
    task1 = habit.tasks[0]
    task2 = habit.add_task(description="Jogging task 2", start_date=habit.created_at + timedelta(days=1), end_date=habit.created_at + timedelta(days=2))
    task_service.complete_task(user.id, task1.id)
    task_service.complete_task(user.id, task2.id)

    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['longest-streak', '--token', token])
    assert result.exit_code == 0
    assert "User David has the longest streak of 2 days for habit Jogging." in result.output


# Test for longest streak for a habit
def test_longest_streak_for_habit(runner, db_session):
    user_service = UserService(db_session)
    user = user_service.register(name="Alice", email="alice1@example.com", password="P@assword123", should_commit=True)

    habit_service = HabitService(db_session)
    habit = habit_service.create_habit(user=user, name="Yoga", periodicity="daily", should_add_task=True)

    task_service = TaskService(db_session)
    task1 = habit.tasks[0]
    task2 = habit.add_task(description="Yoga task 2", start_date=habit.created_at + timedelta(days=1), end_date=habit.created_at + timedelta(days=2))
    task_service.complete_task(user.id, task1.id)
    task_service.complete_task(user.id, task2.id)

    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['longest-streak-for-habit', '--token', token, '--habit_id', habit.id])
    assert result.exit_code == 0
    assert "User Alice has the longest streak of 2 days for habit Yoga." in result.output


# Test for deleting a habit
def test_delete_habit(runner, db_session):
    user_service = UserService(db_session)
    user = user_service.register(name="Frank", email="frank1@example.com", password="P@assword123", should_commit=True)

    habit_service = HabitService(db_session)
    habit = habit_service.create_habit(user=user, name="Cycling", periodicity="weekly", should_add_task=True)

    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['delete-habit', '--token', token, '--habit_id', habit.id])
    assert result.exit_code == 0
    assert "Habit Cycling deleted successfully!" in result.output

# Test for current_habits (list all habits)
def test_current_habits(runner, db_session):
    # Register a user
    user_service = UserService(db_session)
    user = user_service.register(name="Alice", email="alice2@example.com", password="P@assword123", should_commit=True)

    # Create habits for the user
    habit_service = HabitService(db_session)
    habit_service.create_habit(user=user, name="Exercise", periodicity="daily", should_add_task=True)
    habit_service.create_habit(user=user, name="Read", periodicity="weekly", should_add_task=True)

    # Run the current_habits command
    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['current-habits', '--token', token])
    assert result.exit_code == 0
    assert "Exercise" in result.output  # Check that the habit "Exercise" appears
    assert "Read" in result.output  # Check that the habit "Read" appears


# Test for current_habits_for_period (list habits filtered by period)
def test_current_habits_for_period(runner, db_session):
    # Register a user
    user_service = UserService(db_session)
    user = user_service.register(name="Bob", email="bob12345678@example.com", password="pS#ssword123", should_commit=True)

    # Create habits for the user
    habit_service = HabitService(db_session)
    habit_service.create_habit(user=user, name="Jogging", periodicity="daily", should_add_task=True)
    habit_service.create_habit(user=user, name="Cooking", periodicity="weekly", should_add_task=True)
    habit_service.create_habit(user=user, name="Reading", periodicity="fortnightly", should_add_task=True)

    # Test for daily period
    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['current-habits-for-period', '--token', token, '--period', 'daily'])
    assert result.exit_code == 0
    assert "Jogging" in result.output  # Habit with daily periodicity should be listed
    assert "Cooking" not in result.output  # Habit with weekly periodicity should not be listed

    # Test for weekly period
    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['current-habits-for-period', '--token', token, '--period', 'weekly'])
    assert result.exit_code == 0
    assert "Cooking" in result.output  # Habit with weekly periodicity should be listed
    assert "Jogging" not in result.output  # Habit with daily periodicity should not be listed

    # Test for fortnightly period
    token = user_service.get_auth_token(user.email)
    result = runner.invoke(cli, ['current-habits-for-period', '--token', token, '--period', 'fortnightly'])
    assert result.exit_code == 0
    assert "Reading" in result.output  # Habit with fortnightly periodicity should be listed
    assert "Jogging" not in result.output  # Habit with daily periodicity should not be listed
