# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker caching
COPY services/sqlite-kafka-sync/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Correct paths since "core" is in the build context
COPY core /app/core

# Copy only necessary application files
COPY services/sqlite-kafka-sync/sqlite_to_kafka.py /app/sqlite_to_kafka.py

# Set environment variables
ENV SQLITE_DB="sensor_data.db"
ENV SQLITE_TABLE="sensor_data"
ENV KAFKA_BROKER="kafka:9092"
ENV KAFKA_TOPIC="sensor_data"

# Run the script
CMD ["python", "/app/sqlite_to_kafka.py"]