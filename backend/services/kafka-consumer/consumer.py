import json
import os
from kafka import KafkaConsumer
from sqlalchemy.orm import sessionmaker
from core.database import engine
from core.models import SensorData

# Kafka Config
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

# Database Session
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def consume_messages():
    """Consume messages from Kafka and store in PostgreSQL"""
    for message in consumer:
        data = message.value
        print(f"Received data: {data}")

        # Insert into PostgreSQL
        new_entry = SensorData(
            device_id=data["device_id"],
            sensor_type=data["sensor_type"],
            value=json.dumps(data["value"]),
            timestamp=data["timestamp"]
        )
        db.add(new_entry)
        db.commit()
        print(f"Stored in PostgreSQL: {data}")

if __name__ == "__main__":
    print(f"Listening for Kafka topic: {KAFKA_TOPIC}")
    consume_messages()