FROM python:3.9.6-slim-buster

# Install PostgreSQL dependencies needed for psycopg2 installation
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
RUN pip install -r requirements.txt

# Copy your application code into the container
COPY . .

# Sets alembic DB url and runs migrations
RUN python configure_alembic.py

# Create the initial data
RUN make init_data

# RUN the habit tracker script in deamon mode
CMD ["make", "schedule"]
