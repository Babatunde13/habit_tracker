from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, types, func
from sqlalchemy.orm import relationship
from datetime import datetime
import bcrypt
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
    created_at = Column(types.DateTime, nullable=False, default=func.now())
    updated_at = Column(types.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    completed = Column(Boolean, default=False)
    completed_at = Column(types.DateTime, nullable=True)  # Timestamp for when the task was completed
    habit_id = Column(Integer, ForeignKey('habits.id'))

    habit = relationship('Habit', back_populates='tasks')

    def complete(self):
        """Mark task as completed and set the completion timestamp."""
        self.completed = True
        self.completed_at = datetime.now()

    def uncomplete(self):
        """Mark task as uncompleted and reset the completion timestamp."""
        self.completed = False
        self.completed_at = None

class HabitEvent(Base):
    __tablename__ = 'habit_events'

    id = Column(Integer, primary_key=True)
    created_at = Column(types.DateTime, nullable=False, default=func.now())
    updated_at = Column(types.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    date = Column(types.DateTime, nullable=False, default=func.now())
    completed = Column(Boolean, default=False)
    habit_id = Column(Integer, ForeignKey('habits.id'))

    habit = relationship('Habit', back_populates='habit_events')

class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(types.DateTime, nullable=False, default=func.now())
    updated_at = Column(types.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    periodicity = Column(String, nullable=False)  # daily, weekly, etc.
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='habits')
    habit_events = relationship('HabitEvent', back_populates='habit', cascade='all, delete-orphan')
    tasks = relationship('Task', back_populates='habit', cascade='all, delete-orphan')

    def get_streak(self) -> int:
        """Dynamically compute the streak based on habit events."""
        streak = 0
        for event in reversed(self.habit_events):
            if event.completed:
                streak += 1
            else:
                break
        return streak

    def add_event(self, completed: bool):
        """Add a new habit event (check-off) for today."""
        event = HabitEvent(habit_id=self.id, completed=completed, date=datetime.now())
        self.habit_events.append(event)

    def get_tasks(self):
        """Get all tasks associated with the habit."""
        return self.tasks
