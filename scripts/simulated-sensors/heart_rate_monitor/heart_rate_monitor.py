import paho.mqtt.client as mqtt
import sqlite3
import json
import time
import os
import argparse
import math
import random

# MQTT Configuration
MQTT_BROKER = "localhost"  # Change to "mosquitto_broker" if running inside Docker
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/heart_rate_monitor"

# SQLite Configuration
SQLITE_DB = os.environ.get("SQLITE_DB", "/var/lib/sqlite/heart_rate_data.db")

# Heart Rate Simulation Parameters
BASE_HEART_RATE = 70  # Average resting heart rate
HEART_RATE_VARIATION = 15  # Max fluctuation range for heart rate
PERIOD = 30  # Seconds for a full cycle (sine wave effect)
ALERT_THRESHOLD = 120  # Heart rate above this may trigger an alert

# Simulated Network Behavior
SIMULATED_DISCONNECT_TIME = 20  # Time in seconds to go offline
SIMULATED_RECONNECT_TIME = 30  # Time in seconds to come back online

def publish_to_mqtt(data):
    """Publish data to the MQTT broker."""
    try:
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.publish(MQTT_TOPIC, json.dumps(data))
        client.disconnect()
        print(f"✅ ONLINE: Published to MQTT: {data}")
        return True
    except Exception as e:
        print(f"❌ OFFLINE: Cannot publish to MQTT, saving to SQLite. Error: {e}")
        return False

def save_to_sqlite(data):
    """Save sensor data to SQLite when offline."""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    # Ensure the table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS heart_rate_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            sensor_type TEXT NOT NULL,
            value TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            synced INTEGER DEFAULT 0
        );
    """)

    # Insert new data
    cursor.execute("""
        INSERT INTO heart_rate_data (device_id, sensor_type, value, synced)
        VALUES (?, ?, ?, 0)
    """, (data["device_id"], data["sensor_type"], json.dumps(data["value"])))

    conn.commit()
    conn.close()
    print(f"💾 OFFLINE: Saved to SQLite: {data}")

def sync_offline_data():
    """Syncs offline data to MQTT once the device is back online."""
    print("🔄 ONLINE: Syncing unsynced SQLite data to MQTT...")

    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    # Fetch unsynced data
    cursor.execute("SELECT id, device_id, sensor_type, value, timestamp FROM heart_rate_data WHERE synced = 0")
    unsynced_data = cursor.fetchall()

    for row in unsynced_data:
        record_id, device_id, sensor_type, value, timestamp = row
        data = {
            "device_id": device_id,
            "sensor_type": sensor_type,
            "value": json.loads(value),
            "timestamp": timestamp
        }

        # If successfully published to MQTT, mark as synced
        if publish_to_mqtt(data):
            cursor.execute("UPDATE heart_rate_data SET synced = 1 WHERE id = ?", (record_id,))
            conn.commit()
            print(f"🔄 SYNCED: {data}")

    conn.close()

def main(force_offline):
    t = 0  # Time counter for heart rate simulation
    online = True  # Start in online mode

    while True:
        # Simulate heart rate using a sine wave pattern with small randomness
        heart_rate = BASE_HEART_RATE + HEART_RATE_VARIATION * math.sin((2 * math.pi / PERIOD) * t) + random.uniform(-5, 5)
        heart_rate = round(heart_rate, 1)  # Round for realism
        alert = heart_rate > ALERT_THRESHOLD  # Trigger alert if heart rate is too high

        sensor_data = {
<<<<<<< HEAD
            "device_id": "device_hrm_001",
=======
            "device_id": "device_heart_01",
>>>>>>> 24e5288 (Added new modifications)
            "sensor_type": "heart_rate_monitor",
            "value": {
                "heart_rate": heart_rate,
                "alert": alert
            },
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Simulated Network Conditions
        if not force_offline:
            if t % (SIMULATED_DISCONNECT_TIME + SIMULATED_RECONNECT_TIME) < SIMULATED_DISCONNECT_TIME:
                online = False
                print("❌ SIMULATED: Sensor is offline.")
            else:
                online = True
                print("✅ SIMULATED: Sensor is back online.")

        # Decide where to send data
        if online and not force_offline:
            publish_to_mqtt(sensor_data)
            sync_offline_data()  # Sync only when online
        else:
            save_to_sqlite(sensor_data)

        t += 1  # Increment time counter
        time.sleep(1)  # Simulate delay between readings

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulated Heart Rate Monitor")
    parser.add_argument("--offline", action="store_true", help="Force offline mode (saves to SQLite only)")
    args = parser.parse_args()

    main(args.offline)