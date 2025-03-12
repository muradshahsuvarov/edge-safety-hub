import paho.mqtt.client as mqtt
import json
import requests

import os

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("MQTT_TOPIC", "sensors/data")

TOPIC = "sensors/data"

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode("utf-8"))
    requests.post("http://data-ingestion:8000/ingest", json=payload)

client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)
client.loop_start()
