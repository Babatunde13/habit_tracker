
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  install         Install dependencies"
	@echo "  migrate-up      Migrate up"
	@echo "  migrate-down    Migrate down"
	@echo "  migrate-revision Create migration revision"
	@echo "  migrate-show    Show migration history"
	@echo "  schedule        Run habit tracker"
	@echo "  init_data       Initialize database"
	@echo "  cli             Run CLI"

.PHONY: install
install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

.PHONY: migrate-up
migrate-up:
#	@echo "Migrating up..."
	@echo "Migrating up..."
	alembic upgrade head

.PHONY: migrate-down
migrate-down:
#	@echo "Migrating down..."
	@echo "Migrating down..."
	alembic downgrade -1

.PHONY: migrate-revision
migrate-revision:
#	@echo "Creating migration revision..."
	@echo "Creating migration revision..."
	@read -p "Enter revision message: " message; \
	alembic revision --autogenerate -m "$$message"

.PHONY: migrate-show
migrate-show:
#	@echo "Show migration history..."
	@echo "Show migration history..."
	alembic history

.PHONY: schedule
schedule:
	@echo "Running habit tracker..."
	python habit_tracker.py

.PHONY: init_data
init_data:
	@echo "Initializing database..."
	python init_data.py 

.PHONY:cli
cli:
	@echo "Running CLI..."
	python cli.
