# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY ./services/kafka-consumer/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Correctly copy the entire core folder (including database.py)
COPY ./core /app/core

# ✅ Ensure Python can find the core module
ENV PYTHONPATH="/app"

# Copy only necessary application files
COPY ./services/kafka-consumer/consumer.py /app/consumer.py

# Set environment variables
ENV KAFKA_BROKER="kafka:9092"
ENV KAFKA_TOPIC="sensor_data"
ENV DATABASE_URL="postgresql://postgres:postgres@postgres_db:5432/sensors_db"

# Run the script
CMD ["python", "/app/consumer.py"]