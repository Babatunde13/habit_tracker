import schedule
import time
from datetime import datetime
from app.services.habit_service import HabitService
from app.services.util import is_in_range
from app.database import SessionLocal, init_db
from app.models import Habit

# Initialize the database
init_db()

def track_missed_tasks():
    """Scheduled task to track missed tasks at midnight."""
    db = SessionLocal()
    habit_service = HabitService(db)

    # Iterate over all habits and mark missed tasks as incomplete
    habits = db.query(Habit).all()
    for habit in habits:
        today = datetime.now().date()

        completed_in_range = any(is_in_range(habit, event) for event in habit.habit_events)
        if not completed_in_range:
            # Mark missed habit event
            habit_service.add_event(habit, completed=False)
            print(f"Missed task for habit {habit.name} on {today}. Event added.")

    db.commit()
    db.close()

# Schedule the task to run at midnight every day (host machine timezone)
schedule.every().day.at("00:00").do(track_missed_tasks)

# Keep the script running and periodically check for scheduled tasks
if __name__ == "__main__":
    print("Scheduler started. Waiting for midnight...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
