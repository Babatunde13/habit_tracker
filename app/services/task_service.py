from app.models import Task, Habit
from sqlalchemy.orm import Session
from app.services.habit_service import HabitService

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, habit: Habit, description: str):
        """Create a new task for a habit."""
        task = Task(description=description, completed=False, habit=habit)
        return task

    def complete_task(self, user_id: int, task_id: int):
        """Mark task as completed and update habit event."""
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.complete()  # Mark the task as completed
            habit = task.habit
            if habit.user_id != user_id:
                raise ValueError("Task does not belong to the user.")
            habit_service = HabitService(self.session)
            habit_service.add_event(habit, completed=True)  # Create a completed habit event
            self.session.commit()
        return task

    def uncomplete_task(self, user_id: int, task_id: int):
        """Mark task as uncompleted and update habit event."""
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.uncomplete()  # Mark the task as uncompleted
            habit = task.habit
            if habit.user_id != user_id:
                raise ValueError("Task does not belong to the user.")
            habit_service = HabitService(self.session)
            habit_service.add_event(habit, completed=False)  # Create an uncompleted habit event
            self.session.commit()
        return task

    def get_task_by_id(self, task_id: int):
        """Retrieve a task by its ID."""
        return self.session.query(Task).filter(Task.id == task_id).first()

    def get_tasks_for_habit(self, habit: 'Habit'):
        """Get all tasks for a given habit."""
        return habit.tasks
