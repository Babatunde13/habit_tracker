from ..models import Task
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
