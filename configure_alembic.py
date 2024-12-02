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

if __name__ == "__main__":
    set_db_url()