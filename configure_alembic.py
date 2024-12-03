from app.config import config

def set_db_url():
    # open the alembic.ini file replace the line that starts with "sqlalchemy.url" with the following line
    with open("alembic.ini", "r") as f:
        lines = f.readlines()
    with open("alembic.ini", "w") as f:
        for line in lines:
            if line.startswith("sqlalchemy.url"):
                f.write(f"sqlalchemy.url = {config.DATABASE_URL}\n")
            else:
                f.write(line)

def migrate_up():
    # run the following command in the terminal to migrate the database
    # alembic upgrade head
    from os import system
    system("alembic upgrade head")

if __name__ == "__main__":
    set_db_url()
    migrate_up()
