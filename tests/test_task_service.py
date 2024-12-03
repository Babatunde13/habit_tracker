import pytest
from app.services.task_service import TaskService
from app.models import User

def test_complete_task_valid(db_session, sample_user, sample_task):
    """Test completing a task with valid user and task."""
    task_service = TaskService(db_session)

    # Verify that the task is initially not completed
    assert sample_task.completed is False

    # Call the complete_task method to mark the task as completed
    completed_task = task_service.complete_task(sample_user.id, sample_task.id)

    # Verify that the task was marked as completed
    assert completed_task.completed is True
    assert completed_task.completed_at is not None  # Task completion timestamp should be set


def test_complete_task_invalid_user(db_session, sample_user, sample_task):
    """Test completing a task with an invalid user (task doesn't belong to user)."""
    task_service = TaskService(db_session)

    # Create a new user for the invalid case
    another_user = User(name="Another User", email="anotheruser@example.com")
    another_user.set_password("password123")
    db_session.add(another_user)
    db_session.commit()

    # Try to complete the task with a different user (should raise ValueError)
    with pytest.raises(ValueError, match="Task does not belong to the user."):
        task_service.complete_task(another_user.id, sample_task.id)


def test_complete_task_task_not_found(db_session, sample_user):
    """Test completing a task that does not exist."""
    task_service = TaskService(db_session)

    # Use a non-existing task ID (a task ID that hasn't been created)
    invalid_task_id = 9999  # Assumed invalid task ID

    # Try to complete the non-existing task (should raise an error or return None)
    task = task_service.complete_task(sample_user.id, invalid_task_id)
    
    # Since the task doesn't exist, it should return None
    assert task is None
