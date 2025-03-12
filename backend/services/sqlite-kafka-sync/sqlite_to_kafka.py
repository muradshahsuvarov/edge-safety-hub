import sqlite3
import json
from kafka import KafkaProducer
import time
import os

# ✅ Read from the local SQLite database (mounted in the container)
SQLITE_DB = os.getenv("SQLITE_DB", "/var/lib/sqlite/sensor_data.db")  # Mounted from local
SQLITE_TABLE = os.getenv("SQLITE_TABLE", "sensor_data")

# ✅ Kafka Configuration (Inside Docker)
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "sensor_data")

# ✅ Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def get_unsynced_data():
    """Fetch unsynced data from SQLite."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    query = f"SELECT id, device_id, sensor_type, value, timestamp FROM {SQLITE_TABLE} WHERE synced=0"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def mark_as_synced(record_id):
    """Mark data as synced in SQLite."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    query = f"UPDATE {SQLITE_TABLE} SET synced=1 WHERE id=?"
    cursor.execute(query, (record_id,))
    conn.commit()
    conn.close()

def sync_data_to_kafka():
    """Read unsynced data from SQLite and publish it to Kafka."""
    while True:
        data = get_unsynced_data()
        if not data:
            print(f"No unsynced data in table `{SQLITE_TABLE}`. Sleeping...")
            time.sleep(10)  # Sleep before checking again
            continue

        for record in data:
            record_id, device_id, sensor_type, value, timestamp = record
            message = {
                "device_id": device_id,
                "sensor_type": sensor_type,
                "value": json.loads(value),  # Parse JSON
                "timestamp": timestamp
            }

            # ✅ Send to Kafka
            producer.send(KAFKA_TOPIC, message)
            print(f"✅ Sent {message} to Kafka topic `{KAFKA_TOPIC}`")

            # ✅ Mark as synced in SQLite
            mark_as_synced(record_id)

if __name__ == "__main__":
    print(f"🚀 Using SQLite table `{SQLITE_TABLE}` and Kafka topic `{KAFKA_TOPIC}`")
    sync_data_to_kafka()