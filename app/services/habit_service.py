from ..models import User, Habit
from .util import compute_start_and_end_date
from datetime import datetime
from sqlalchemy.orm import Session

class HabitService:
    def __init__(self, session: Session):
        self.session = session

    def create_habit(self, user, name: str, periodicity: str, created_at=None, should_add_task=True):
        """Create a new habit for a user."""
        habit = Habit(name=name, periodicity=periodicity, user=user, created_at=created_at or datetime.now())
        self.session.add(habit)
        if should_add_task:
            self.add_task(habit)  # Add a task for current period
        return habit

    def get_habit_task_end_date(self, habit: Habit):
        return compute_start_and_end_date(habit.periodicity)

    def add_task(self, habit: Habit, should_commit=True):
        """Add a task for the habit for the period."""
        start_date, end_date = self.get_habit_task_end_date(habit)
        tasksLen = len(habit.tasks)
        description = f"{habit.name} task {tasksLen + 1}"
        task = habit.add_task(description, start_date, end_date)
        self.session.add(task)

        if should_commit:
            self.session.commit()
        return task

    def update_habit(self, habit: Habit, name: str):
        """Update the name and periodicity of a habit."""
        habit.name = name
        self.session.commit()

    def get_current_streaks(self, habit: Habit):
        """Get the current streak for a habit based on task completion."""
        return habit.get_current_streaks()
    
    def get_longest_streaks(self, habit: Habit):
        """Get the current streak for a habit based on task completion."""
        return habit.get_longest_streaks()

    def get_habit(self, user_id: int, habit_id: int):
        """Retrieve a habit by its ID."""
        return self.session.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user_id).first()

    def get_user_habits(self, user: User):
        """Get all habits of a user."""
        return user.habits
    
    def get_all_habits(self):
        """Get all habits."""
        return self.session.query(Habit).all()

    def delete_habit(self, id: int, user: User):
        # Fetch the habit for the given id and user
        habit = self.session.query(Habit).filter(Habit.id == id, Habit.user_id == user.id).first()

        # Raise an error if the habit does not exist
        if not habit:
            raise ValueError("Habit does not exist")

        # Delete all associated tasks for the habit
        for task in habit.tasks:
            self.session.delete(task)

        self.session.delete(habit)
        self.session.commit()

    def get_user_habits_for_period(self, user_id: int, period: str=None):
        """Retrieve habits for the current period (daily/weekly/fortnightly/monthly/biannually/yearly)."""
        if period == None:
            habits = self.session.query(Habit).filter(Habit.user_id == user_id).all()
        else:
            habits = self.session.query(Habit).filter(Habit.periodicity == period.lower(), Habit.user_id == user_id).all()
        return habits
