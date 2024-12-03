# Test HabitService create_habit method
def test_create_habit(habit_service, sample_user):
    habit = habit_service.create_habit(user=sample_user, name="Exercise", periodicity="daily")
    
    # Check that the habit was created correctly
    assert habit.name == "Exercise"
    assert habit.periodicity == "daily"
    assert habit.user_id == sample_user.id
    assert habit.id is not None  # Habit should have been assigned an ID


# Test HabitService add_task method
def test_add_task(habit_service, sample_user):
    habit = habit_service.create_habit(user=sample_user, name="Exercise", periodicity="daily")
    # Check that a task has been added
    assert len(habit.tasks) == 1
    task = habit.tasks[0]
    assert task.description == "Exercise task 1"
    assert task.completed is False  # The task should not be marked as completed by default


# Test HabitService update_habit method
def test_update_habit(habit_service, sample_user):
    habit = habit_service.create_habit(user=sample_user, name="Exercise", periodicity="daily")
    
    # Update the habit name
    habit_service.update_habit(habit, name="Jogging")
    
    # Verify that the habit's name was updated
    updated_habit = habit_service.get_habit(sample_user.id, habit.id)
    assert updated_habit.name == "Jogging"


# Test HabitService get_current_streaks method
def test_get_current_streaks(habit_service, sample_user):
    habit = habit_service.create_habit(user=sample_user, name="Exercise", periodicity="daily")

    # Mark the task as completed
    task = habit.tasks[0]
    task.complete()

    # Get the current streak
    streak = habit_service.get_current_streaks(habit)
    
    # Check that the streak is 1 after completing the task
    assert streak == 1


# Test HabitService delete_habit method
def test_delete_habit(habit_service, sample_user):
    habit = habit_service.create_habit(user=sample_user, name="Exercise", periodicity="daily")
    
    # Ensure the habit was created
    assert habit is not None
    
    # Delete the habit
    habit_service.delete_habit(habit.id, sample_user)
    
    # Try to retrieve the deleted habit, should return None
    deleted_habit = habit_service.get_habit(sample_user.id, habit.id)
    assert deleted_habit is None


# Test HabitService get_user_habits_for_period method
def test_get_user_habits_for_period(habit_service, sample_user):
    habit_service.create_habit(user=sample_user, name="Exercise", periodicity="daily")
    habit_service.create_habit(user=sample_user, name="Reading", periodicity="weekly")
    
    # Retrieve daily habits
    daily_habits = habit_service.get_user_habits_for_period(sample_user.id, "daily")
    assert len(daily_habits) == 1
    assert daily_habits[0].name == "Exercise"

    # Retrieve weekly habits
    weekly_habits = habit_service.get_user_habits_for_period(sample_user.id, "weekly")
    assert len(weekly_habits) == 1
    assert weekly_habits[0].name == "Reading"


# Test HabitService get_all_habits method
def test_get_all_habits(habit_service, sample_user):
    habit_service.create_habit(user=sample_user, name="Exercise", periodicity="daily")
    habit_service.create_habit(user=sample_user, name="Reading", periodicity="weekly")
    
    all_habits = habit_service.get_all_habits()
    
    assert len(all_habits) > 0  # Should return at least the habits we created in the test
