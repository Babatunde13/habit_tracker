import time
import schedule
from app.services.habit_service import HabitService
from app.database import SessionLocal, init_db

def create_new_task_for_habits():
    """Scheduled task to create a new task for all habits."""
    db = SessionLocal()
    habit_service = HabitService(db)
    habits = habit_service.get_all_habits()
    for habit in habits:
        task = habit_service.add_task(habit, False)
        print(f"New task created for habit {habit.name} with periodicity {habit.periodicity}")

    db.commit()
    db.close()

# Schedule the task to run at midnight every day (host machine timezone)
schedule.every().day.at("00:00").do(create_new_task_for_habits)

# Keep the script running and periodically check for scheduled tasks
if __name__ == "__main__":
    # Initialize the database
    init_db()

    print("Scheduler started. Waiting for midnight...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
