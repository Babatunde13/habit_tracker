from ..models import Task, Habit
from sqlalchemy.orm import Session

class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def complete_task(self, user_id: int, task_id: int):
        """Mark task as completed and update habit event."""
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            habit = task.habit
            if habit.user_id != user_id:
                raise ValueError("Task does not belong to the user.")
            task.complete()  # Mark the task as completed
            self.session.commit()
        return task

    def uncomplete_task(self, user_id: int, task_id: int):
        """Mark task as uncompleted and update habit event."""
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            habit = task.habit
            if habit.user_id != user_id:
                raise ValueError("Task does not belong to the user.")
            task.uncomplete()  # Mark the task as uncompleted
            self.session.commit()
        return task

    def get_task_by_id(self, task_id: int):
        """Retrieve a task by its ID."""
        return self.session.query(Task).filter(Task.id == task_id).first()

    def get_tasks_for_habit(self, habit: 'Habit'):
        """Get all tasks for a given habit."""
        return habit.tasks
