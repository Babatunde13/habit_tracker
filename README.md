# Habit Tracker Application

## Overview

The **Habit Tracker Application** allows users to create, track, and manage their habits. The app has a Command Line Interface (CLI) for interacting with the backend, which enables user registration, habit creation, task management, and provides analytics for habits.

![Arch Diagram](./habit_tracker.drawio.png)

### Features:
- **User Registration** and **Login**.
- **Create and Manage Habits**.
- **Add and List Tasks**.
- **Track Habit Streaks and Analytics**.
- **Leaderboard** for tracking the top users by their habit streaks.
- **Scheduler** for running scheduled tasks like tracking missed habits and updating habit streaks.

## Installation

You can set up the application using **Docker** or **Manually**. Both methods will set up the database, create dummy data, and configure the scheduler.

### 1. **Installation via Docker**

**Requirements**:
- Docker
- Docker Compose

#### Steps to Install and Run:

1. **Clone the Repository**:

    # Habit Tracker Application

## Overview

The **Habit Tracker Application** allows users to create, track, and manage their habits. The app has a Command Line Interface (CLI) for interacting with the backend, which enables user registration, habit creation, task management, and provides analytics for habits. When a new habit is created we immediately create a task for it to track for current period. I also setup a scheduler that runs every morning at 12am to create tasks at the beginning of the next period.

### Features:
- **User Registration** and **Login**.
- **Create and Manage Habits**.
- **List and Complete Tasks**.
- **Track Habit Streaks and Analytics**.
- **Leaderboard** for tracking the top users by their habit streaks.
- **Scheduler** for running scheduled tasks like tracking missed habits and updating habit streaks.

## Installation

You can set up the application **Manually**. This will create dummy data, and configure the scheduler. But before we do this we need to have our PostgreSQL database ready. If you already have one you can skip the next step, otherwise you can setup your database using Docker and docker compose

### 1. **Installation Of Postgres via Docker**

**Requirements**:
- Docker
- Docker Compose

#### Steps to Install and Run:

1. **Clone the Repository**:

   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Build and Run the Application**:
   Run the following command to set up the database in the background:

   ```
   docker-compose up -d
   ```

   This command does the following:
   - **Sets up the PostgreSQL database**.
   - **The database URL will be postgresql://tracker:tracker@localhost:5432/tracker** as defined in the Docker compose file.


### 2. **Setting Up the Application**

**Requirements**:
- PostgreSQL Database
- Python 3.9+

#### Steps to Install:

1. **Setup your virtual environment, this can vary depending on your OS**:
    In the same directory

   ```bash
   pip install --upgrade pip
   pip install virtualenv # creates virtual environment
   . venv/bin/activate # or .\\venv\\Scripts\\Activate to activate virtual environment
   ```

   ##### Install dependencies
   ```bash
   pip install -r requirements.txt # install dependencies
   ```
   

2. **Set Up the PostgreSQL Database**:
   - If you have your PostgreSQL database copy your database URL, it should be in the form `postgresql://<username>:<password>@<host>:<port>/<dbname>` or you used the step for Docker above, the db URL will be `postgresql://tracker:tracker@localhost:5432/tracker`. Put this in your `.env` file
   - Setup your test database URL, this will be used for testing purpose, If you have your PostgreSQL Database or you used the Docker step above, you can run the `create_test_db.sh` script, ensure the username, host and database name for your primary db is correct(The data in the file matches the Docker config). Running the script should prompt you for a password, this is the password of your Primary database, for the Docker setup this is `tracker`. Use the database name `tracker_test` to construct your test Database URL e.g postgresql://tracker:tracker@localhost:5432/tracker_test
   - Ensure you have the environment variables set as defined in the `.env.sample` file:
   ```
   DATABASE_URL=postgresql://tracker:tracker@localhost:5432/tracker
   TEST_DATABASE_URL=postgresql://tracker:tracker@localhost:5432/tracker_test
   ENV=production
   SECRET_KEY=secret
   ```
   Change `SECRET_KEY` to something more difficult to guess. If ENV is production it removes debug logs from the console when running the application. During testing the ENV is forces to `test` automatically.


3. **Run Migrations**:

   ```bash
   python configure_alembic.py # sets the db url inside the alembic.ini file based on the DATABASE_URL env and runs migration
   ```

   This command will run the necessary migrations to set up the database schema.

4. **Initialize Dummy Data**:

   Once the migrations are complete, run:

    ```bash
   python init_data.p
   ```

   This will insert some dummy data into the database for testing purposes.

5. **Run the Scheduler**:

   The scheduler will be used to automatically create new tasks for habits at the start of next period:
   Run this in a new terminal(same directory), as it will not stop. We can also run this script in the background, this approach vary depending on the OS.

    ```bash
   python scheduler.py
   ```

6. **Run the Application**:

   You can now run the CLI commands as described below.

### 3. **Running CLI Commands**

After setting up the environment (either via Docker or manually), you can interact with the application using the CLI.

To view the available commands, run:

```bash
python client.py help
```

### CLI Commands Overview

Sample data are generated using the `init_data.py` script. To login with any of the dummy user, there is a `user` dictionary in [./init_data.py](./init_data.py#L8) use any email and password to authenticate.

Here is an explanation of the available commands in the Habit Tracker CLI(client):

#### 1. **`register`**: Register a new user

```bash
python client.py register
```

**Options**:
- `--name`: Your name (required)
- `--email`: Your email address (required)
- `--password`: Your password (required)

This command registers a new user in the system.

#### 2. **`login`**: Log in to an existing user account

```bash
python client.py login
```

**Options**:
- `--email`: Your email address (required)
- `--password`: Your password (required)

This command logs in a user and provides the authentication token for further operations.

#### 3. **`update-password`**: Update user password

```bash
python client.py update-password
```

**Options**:
- `--email`: Your email address (required)
- `--old_password`: Your current password (required)
- `--new_password`: Your new password (required)

This command allows the user to change their password.

#### 4. **`create-habit`**: Create a new habit

```bash
python client.py create-habit
```

**Options**:
- `--token`: The auth token of the user (required)
- `--name`: Name of the habit (required)
- `--periodicity`: How often the habit should occur (daily, weekly, etc.) (required)

This command creates a new habit for the user and the first task for the habit.

#### 5. **`list-habits`**: List all habits of a user

```bash
python client.py list-habits
```

**Options**:
- `--token`: The auth token of the user (required)

This command lists all habits of the user.

#### 6. **`list-tasks`**: List all tasks of a habit

```bash
python client.py list-tasks
```

**Options**:
- `--token`: The auth token of the user (required)
- `--habit_id`: The ID of the habit (required)

This command lists all tasks for a given habit.

#### 7. **`complete-task`**: Mark a task as completed

```bash
python client.py complete-task
```

**Options**:
- `--token`: The auth token of the user (required)
- `--task_id`: The ID of the task to mark as completed (required)

This command marks a task as completed.

#### 8. **`show-current-streaks`**: Show current streaks for all habits

```bash
python client.py show-current-streaks
```

**Options**:
- `--token`: The auth token of the user (required)

This command shows the current streaks for all habits associated with the user.

#### 9. **`longest-streak`**: Show the user's longest streak

```bash
python client.py longest-streak
```

**Options**:
- `--token`: The auth token of the user (required)

This command shows the longest streak for any of the user's habits.

#### 10. **`current-habits-for-period`**: Show current habits for a given period (e.g., weekly, monthly)

```bash
python client.py current-habits-for-period
```

**Options**:
- `--token`: The auth token of the user (required)
- `--period`: The period to check habits for (daily, weekly, etc.) (required)

This command shows the current habits based on the specified period.

#### 11. **`struggled-habits`**: Show the habits you struggled with the most in the last period

```bash
python client.py struggled-habits
```

**Options**:
- `--token`: The auth token of the user (required)
- `--period`: The period to check habits for (daily, weekly, etc.) (required)

This command shows the habits you struggled with the most in the last specified period.

#### 12. **`leaderboard`**: Show the leaderboard based on the longest streaks

```bash
python client.py leaderboard
```

This command shows the top users with the longest streaks.

#### 12. **`delete-habit`**: Show the leaderboard based on the longest streaks

```bash
python client.py delete-habit
```

**Options**:
- `--token`: The auth token of the user (required)
- `--habit_id`: The ID of the habit (required)

This command deletes a user's habit and all it's tasks.

#### 13. **`update-habit`**: Show the leaderboard based on the longest streaks

```bash
python client.py update-habit
```

**Options**:
- `--token`: The auth token of the user (required)
- `--name`: The new name of the habit (required)
- `--habit_id`: The ID of the habit (required)

This command updates a user's existing habit.

#### 14. **`current-habits`**: Show current habits

```bash
python client.py current-habits
```

**Options**:
- `--token`: The auth token of the user (required)

#### 15. **`longest-streak-for-habit`**: Show longest streak for a given habit

```bash
python client.py longest-streak-for-habit
```

**Options**:
- `--token`: The auth token of the user (required)
- `--habit_id`: The ID of the habit (required)

## Troubleshooting
- **Error: "User not found!"**: Make sure you are using a valid token obtained from the login process.
- **Error: "Habit not found!"**: Ensure the habit ID is correct and belongs to the authenticated user.
- **Error: "Invalid periodicity"**: Ensure you input a valid periodicity value (daily, weekly, forthnightly, monthly, quarterly, bianually or yearly).

## Testing
To run the tests, add a `TEST_DATABASE_URL` and then run `pytest tests/` in your terminal, this will automatically run migrations for your db, set environment to test and then run the app tests.
