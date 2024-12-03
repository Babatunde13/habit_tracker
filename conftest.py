import pytest
from app.database import SessionLocal, init_db
from app.models import User, Habit, Task
from app.services.habit_service import HabitService
from app.services.user_service import UserService
from app.services.util import compute_start_and_end_date
from configure_alembic import set_db_url, migrate_up
import os

# Path to the alembic.ini file (make sure this path is correct)
ALEMBIC_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'alembic.ini')
os.environ['ENV'] = 'test'  # Set the environment to test

def delete_all_data():
    """Delete all data from the database."""
    db = SessionLocal()
    db.query(Task).delete()
    db.query(Habit).delete()
    db.query(User).delete()
    db.commit()
    db.close()

@pytest.fixture(scope='session')
def delete_db_data():
    """Fixture to delete all data from the database before and after the test session."""
    delete_all_data()

@pytest.fixture(scope='session')
def db_session():
    """Fixture to manage the database session for the entire test suite."""

    # Setup: Initialize the database schema and run migrations
    set_db_url()  # Set the database URL in the alembic.ini file
    migrate_up()  # Run the migrations
    init_db()  # Ensure the database schema is created
    delete_all_data()  # Optionally, delete all data from the database

    # Create a session for interacting with the database
    db = SessionLocal()
    yield db  # This allows the test to use the db session

    # Teardown: Cleanup after each test
    db.rollback()  # Rollback the transaction to clean up the test data
    db.close()

@pytest.fixture
def sample_user(db_session):
    """Fixture to create a sample user for testing."""
    delete_all_data()  # Delete all data before creating a new user
    user = User(name="Test User", email="testuser@example.com")
    user.set_password("pasSword@123")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture(autouse=True)
def reset_db_after_test(db_session):
    """Fixture to reset the database after each test."""
    
    # At the start of each test, the session is rolled back to clean any changes
    db_session.rollback()

    yield  # This will execute the test

    # After the test finishes, the transaction is rolled back
    db_session.rollback()


@pytest.fixture(scope='function')
def habit_service(db_session):
    """
    Fixture to provide a HabitService instance for each test.
    The `db_session` fixture will be used to create the service with a valid database session.
    """
    return HabitService(db_session)

@pytest.fixture
def sample_habit(db_session, sample_user):
    """Fixture to create a habit for the sample user."""
    habit = Habit(name="Exercise", periodicity="daily", user=sample_user)
    db_session.add(habit)
    db_session.commit()
    return habit


@pytest.fixture
def sample_task(db_session, sample_habit):
    """Fixture to create a task for the sample habit."""
    task = Task(description="Complete workout", habit=sample_habit)
    start_date, end_date = compute_start_and_end_date(sample_habit.periodicity)
    task.start_date = start_date
    task.end_date = end_date
    db_session.add(task)
    db_session.commit()
    return task

@pytest.fixture
def user_service(db_session):
    """Fixture to create a UserService instance for testing."""
    return UserService(db_session)
