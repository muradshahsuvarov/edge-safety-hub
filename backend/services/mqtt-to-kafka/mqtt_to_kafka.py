import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import json
import time

# MQTT Configuration
MQTT_BROKER = "mosquitto_broker"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/gas_detector"

# Kafka Configuration
KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "sensor_data"

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def on_message(client, userdata, message):
    """Callback for MQTT message reception."""
    data = json.loads(message.payload.decode("utf-8"))
    print(f"Received from MQTT: {data}")

    # Publish to Kafka
    producer.send(KAFKA_TOPIC, data)
    print(f"Sent to Kafka topic `{KAFKA_TOPIC}`: {data}")

def main():
    """Subscribe to MQTT and forward messages to Kafka."""
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)
    
    print(f"Listening for MQTT messages on `{MQTT_TOPIC}` and forwarding to Kafka...")
    client.loop_forever()

if __name__ == "__main__":
    main()