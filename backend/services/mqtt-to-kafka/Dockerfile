# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY ./services/mqtt-to-kafka/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY ./services/mqtt-to-kafka/mqtt_to_kafka.py /app/mqtt_to_kafka.py

# Set environment variables
ENV MQTT_BROKER="mosquitto_broker"
ENV KAFKA_BROKER="kafka:9092"
ENV MQTT_TOPIC="sensor/gas_detector"
ENV KAFKA_TOPIC="sensor_data"

# Run the script
CMD ["python", "/app/mqtt_to_kafka.py"]