FROM python:3.9.6-slim-buster

# Install PostgreSQL dependencies and other packages needed for psycopg2 installation
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt file into the container
COPY requirements.txt .

# Setup dependencies
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt

# Copy your application code into the container
COPY . .

RUN python configure_alembic.py

# run migrations
RUN make migrate-up

# Create the initial data
RUN make init_data

# RUN the habit tracker script in deamon mode
CMD ["make", "schedule"]
