from datetime import datetime
import bcrypt
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, types, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    created_at = Column(types.DateTime, nullable=False, default=func.now())
    updated_at = Column(types.DateTime, nullable=False, default=func.now(), onupdate=func.now()) 
    name = Column(String, nullable=False) 
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Store hashed password

    habits = relationship('Habit', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Hash the password and store it in the password_hash field."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.name}>'

    def __str__(self):
        return self.name

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    start_date = Column(types.DateTime, nullable=False, default=func.now())
    end_date = Column(types.DateTime, nullable=False) # Deadline for the task
    updated_at = Column(types.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    completed = Column(Boolean, default=False)
    completed_at = Column(types.DateTime, nullable=True)  # Timestamp for when the task was completed
    habit_id = Column(Integer, ForeignKey('habits.id'))

    habit = relationship('Habit', back_populates='tasks')

    def complete(self):
        """Mark task as completed and set the completion timestamp."""
        now = datetime.now()
        if now > self.end_date:
            raise ValueError("Task is overdue and cannot be completed.")
        self.completed = True
        self.completed_at = now

    def uncomplete(self):
        """Mark task as uncompleted and reset the completion timestamp."""
        self.completed = False
        self.completed_at = None

class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(types.DateTime, nullable=False, default=func.now())
    updated_at = Column(types.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    periodicity = Column(String, nullable=False)  # daily, weekly, etc.
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='habits')
    tasks = relationship('Task', back_populates='habit', cascade='all, delete-orphan')

    def get_current_streaks(self) -> int:
        """Dynamically compute the streak based on task completion."""
        streak = 0
        for task in reversed(self.tasks):
            if task.completed:
                streak += 1
            else:
                break
        return streak
    
    def get_longest_streaks(self) -> int:
        """Dynamically compute the streak based on task completion."""
        streak = 0
        longest_streak = 0
        for task in reversed(self.tasks):
            if task.completed:
                streak += 1
            else:
                if streak > longest_streak:
                    longest_streak = streak

                streak = 0
        return streak

    def add_task(self, description: str, start_date: datetime, end_date: datetime = None):
        """Add a new task to the habit."""
        task = Task(description=description, completed=False, end_date=end_date, start_date=start_date)
        self.tasks.append(task)
        return task

    def get_tasks(self):
        """Get all tasks associated with the habit."""
        return self.tasks
