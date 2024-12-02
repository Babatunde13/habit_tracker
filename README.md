# Habit Tracker Application

## Overview

The **Habit Tracker Application** allows users to create, track, and manage their habits. The app has a Command Line Interface (CLI) for interacting with the backend, which enables user registration, habit creation, task management, and provides analytics for habits.

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

The **Habit Tracker Application** allows users to create, track, and manage their habits. The app has a Command Line Interface (CLI) for interacting with the backend, which enables user registration, habit creation, task management, and provides analytics for habits.

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

   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Build and Run the Application**:

   Run the following command to set up the database and start the application:

   ```
   docker-compose up -d
   ```

   This command does the following:
   - **Sets up the PostgreSQL database**.
   - **Runs the application**.
   - **Creates dummy data** in the database.
   - **Runs the scheduler** to automatically track missed tasks and update habit streaks.

3. **Access the Application**:

   The application will be available for CLI interaction once the setup is complete. You can run the CLI commands as described below.

### 2. **Manual Installation**

**Requirements**:
- PostgreSQL Database
- Python 3.9+
- Make (optional, but recommended for convenience)

#### Steps to Install:

1. **Clone the Repository and setup dependencies**:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   pip install --upgrade pip
   pip install virtualenv # creates virtual environment
   . venv/bin/activate # or .\\venv\\Scripts\\Activate to activate virtual environment
   pip install -r requirements.txt # install dependencies
   ```

2. **Set Up the PostgreSQL Database**:

   - Create a PostgreSQL database locally (or use any external PostgreSQL instance).
   - Ensure you have the following environment variables set:

    ```bash
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=habit_tracker
     DB_USER=tracker
     DB_PASSWORD=tracker
    ```

3. **Run Migrations**:

   Use `Makefile` commands to set up the database schema:

   ```bash
   make migrate-up
   ```

   This command will run the necessary migrations to set up the database schema.

4. **Initialize Dummy Data**:

   Once the migrations are complete, run:

    ```bash
   make init_data
   ```

   This will insert some dummy data into the database for testing purposes.

5. **Run the Scheduler**:

   The scheduler will track missed tasks and update habit streaks:

    ```bash
   make schedule
   ```

6. **Run the Application**:

   You can now run the CLI commands as described below.

### 3. **Running CLI Commands**

After setting up the environment (either via Docker or manually), you can interact with the application using the CLI.

To view the available commands, run:

```bash
python cli.py help
```

### CLI Commands Overview

Here is an explanation of the available commands in the Habit Tracker CLI:

#### 1. **`register`**: Register a new user

```bash
python cli.py register
```

**Options**:
- `--name`: Your name (required)
- `--email`: Your email address (required)
- `--password`: Your password (required)

This command registers a new user in the system.

#### 2. **`login`**: Log in to an existing user account

```bash
python cli.py login
```

**Options**:
- `--email`: Your email address (required)
- `--password`: Your password (required)

This command logs in a user and provides the authentication token for further operations.

#### 3. **`update-password`**: Update user password

```bash
python cli.py update-password
```

**Options**:
- `--email`: Your email address (required)
- `--old_password`: Your current password (required)
- `--new_password`: Your new password (required)

This command allows the user to change their password.

#### 4. **`create-habit`**: Create a new habit

```bash
python cli.py create-habit
```

**Options**:
- `--token`: The auth token of the user (required)
- `--name`: Name of the habit (required)
- `--periodicity`: How often the habit should occur (daily, weekly, etc.) (required)

This command creates a new habit for the user.

#### 5. **`list-habits`**: List all habits of a user

```bash
python cli.py list-habits
```

**Options**:
- `--token`: The auth token of the user (required)

This command lists all habits of the user.

#### 6. **`add-task`**: Add a task to a habit

```bash
python cli.py add-task
```

**Options**:
- `--token`: The auth token of the user (required)
- `--habit_id`: The ID of the habit (required)
- `--description`: Description of the task (required)

This command allows the user to add a new task to a specific habit.

#### 7. **`list-tasks`**: List all tasks of a habit

```bash
python cli.py list-tasks
```

**Options**:
- `--token`: The auth token of the user (required)
- `--habit_id`: The ID of the habit (required)

This command lists all tasks for a given habit.

#### 8. **`complete-task`**: Mark a task as completed

```bash
python cli.py complete-task
```

**Options**:
- `--token`: The auth token of the user (required)
- `--task_id`: The ID of the task to mark as completed (required)

This command marks a task as completed.

#### 9. **`uncomplete-task`**: Mark a task as uncompleted

```bash
python cli.py uncomplete-task
```

**Options**:
- `--token`: The auth token of the user (required)
- `--task_id`: The ID of the task to mark as uncompleted (required)

This command marks a task as uncompleted.

#### 10. **`show-current-streaks`**: Show current streaks for all habits

```bash
python cli.py show-current-streaks
```

**Options**:
- `--token`: The auth token of the user (required)

This command shows the current streaks for all habits associated with the user.

#### 11. **`longest-streak`**: Show the user's longest streak

```bash
python cli.py longest-streak
```

**Options**:
- `--token`: The auth token of the user (required)

This command shows the longest streak for any of the user's habits.

#### 12. **`current-habits`**: Show habits for a given period (e.g., weekly, monthly)

```bash
python cli.py current-habits
```

**Options**:
- `--token`: The auth token of the user (required)
- `--period`: The period to check habits for (daily, weekly, etc.) (required)

This command shows the current habits based on the specified period.

#### 13. **`struggled-habits`**: Show the habits you struggled with the most in the last period

```bash
python cli.py struggled-habits
```

**Options**:
- `--token`: The auth token of the user (required)
- `--period`: The period to check habits for (daily, weekly, etc.) (required)

This command shows the habits you struggled with the most in the last specified period.

#### 14. **`leaderboard`**: Show the leaderboard based on the longest streaks

```bash
python cli.py leaderboard
```
```bash
python cli.py leaderboard
```
This command shows the top users with the longest streaks.

## Troubleshooting
- **Error: "User not found!"**: Make sure you are using a valid token obtained from the login process.
- **Error: "Habit not found!"**: Ensure the habit ID is correct and belongs to the authenticated user.
- **Error: "Invalid periodicity"**: Ensure you input a valid periodicity value (daily, weekly, etc.).
