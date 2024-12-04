import os
import pytest
from app.database import SessionLocal, init_db
from app.models import User, Habit, Task
from app.services.habit_service import HabitService
from app.services.user_service import UserService
from app.services.util import compute_start_and_end_date
from configure_alembic import set_db_url, migrate_up

@pytest.fixture(scope="session", autouse=True)
def setup():
    """Set the environment to 'test' before running tests."""
    env = os.environ.get('ENV')
    os.environ['ENV'] = 'test'
    from app.config import config

    set_db_url(config.TEST_DATABASE_URL) # Set the database URL for the test database
    migrate_up() # Run migrations before running tests
    yield  # The test runs here
    if env:
        os.environ['ENV'] = env  # Reset the environment variable after the test
    set_db_url() # Reset the database URL to the development database
    

@pytest.fixture(scope='session')
def db_session(setup):
    """Fixture to manage the database session for the entire test suite."""

    # Setup: Initialize the database schema and run migrations
    init_db()  # Ensure the database schema is created

    # Create a session for interacting with the database
    db = SessionLocal()
    yield db  # This allows the test to use the db session

    # Teardown: Cleanup after each test
    db.rollback()  # Rollback the transaction to clean up the test data
    db.close()


@pytest.fixture(scope='function', autouse=True)
def delete_db_data(db_session):
    """Fixture to delete all data from the database before and after the test session."""
    db_session.query(Task).delete()
    db_session.query(Habit).delete()
    db_session.query(User).delete()
    db_session.commit()


@pytest.fixture
def sample_user(db_session):
    """Fixture to create a sample user for testing."""
    user = User(name="Test User", email="testuser@example.com")
    user.set_password("pasSword@123")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture(autouse=True)
def teardown(db_session):
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
