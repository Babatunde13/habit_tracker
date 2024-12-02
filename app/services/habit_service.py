from app.models import Habit, HabitEvent
from sqlalchemy.orm import Session
from datetime import datetime
from app.models import User

class HabitService:
    def __init__(self, session: Session):
        self.session = session

    def create_habit(self, user, name: str, periodicity: str):
        """Create a new habit for a user."""
        habit = Habit(name=name, periodicity=periodicity, user=user)
        return habit

    def add_event(self, habit: Habit, completed: bool):
        """Add an event (check-off) for the habit for today."""
        event = HabitEvent(habit_id=habit.id, completed=completed, date=datetime.now())
        habit.habit_events.append(event)
        self.session.commit()

    def get_streak(self, habit: Habit):
        """Get the current streak for a habit based on habit events."""
        streak = 0
        for event in reversed(habit.habit_events):
            if event.completed:
                streak += 1
            else:
                break
        return streak

    def get_habit(self, user_id: int, habit_id: int):
        """Retrieve a habit by its ID."""
        return self.session.query(Habit).filter(Habit.id == habit_id and Habit.user_id == user_id).first()

    def get_all_habits(self, user: 'User'):
        """Get all habits of a user."""
        return user.habits

    def delete_habit(self, id: int, user: User):
        # Fetch the habit for the given id and user
        habit = self.session.query(Habit).filter(Habit.id == id, Habit.user_id == user.id).first()

        # Raise an error if the habit does not exist
        if not habit:
            raise ValueError("Habit does not exist")

        # Delete all associated tasks for the habit
        # Assuming there is a relationship between Habit and Task, such as Habit.tasks
        for task in habit.tasks:
            self.session.delete(task)

        # Delete all associated events for the habit
        # Assuming there is a relationship between Habit and HabitEvent, such as Habit.habit_events
        for event in habit.habit_events:
            self.session.delete(event)

        # Delete the habit itself
        self.session.delete(habit)

        # Commit the changes to the database
        self.session.commit()
