from datetime import UTC, datetime
import time
import paho.mqtt.client as mqtt
import json
import logging
import random

# Configure logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


class MQTTClient:
    def __init__(self, host, port, username, password, topic):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(self.username, self.password)

        # Register callback functions
        self.client.on_publish = self.on_publish
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    def connect(self, keepalive):
        self.client.connect(self.host, self.port, keepalive)

    def publish(self, message):
        self.client.publish(self.topic, message)

    @staticmethod
    def on_publish(client, userdata, mid, reason_code, properties):
        log.debug(f"Message published with mid: {mid} and reason code: {reason_code}")

    @staticmethod
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            log.debug("MQTT Connected...")

    @staticmethod
    def on_disconnect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            log.debug("Requested disconnect executed successfully")
        else:
            log.debug(f"Unexpected disconnect from MQTT, reason code: {reason_code}")

    @staticmethod
    def on_message(client, userdata, msg):
        log.debug(f"{msg.topic}: {msg.payload.decode()}")


class DataGenerator:
    @staticmethod
    def make_fake_data():
        milliseconds = int(datetime.now(UTC).timestamp() * 1000)
        data = {
            "measurement": "home",
            "tags": {"room": "Living Room"},
            "fields": {
                "temp": random.randint(0, 9000) / 100,
                "hum": random.randint(100, 900) / 10,
                "co": random.randint(0, 200) / 10,
            },
            "timestamp": milliseconds,
        }
        return json.dumps(data)


class Publisher:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def publish_data(self, N=100):
        for _ in range(N):
            message = DataGenerator.make_fake_data()
            self.mqtt_client.publish(message)
            sleep_ms = random.randint(100, 2000) / 1000
            time.sleep(sleep_ms)


if __name__ == "__main__":
    # Define MQTT parameters
    MQTT_HOST = "localhost"  # Replace with your broker's address
    MQTT_PORT = 1883  # Default MQTT port
    MQTT_KEEPALIVE_INTERVAL = 45
    MQTT_TOPIC = "IOT/test"  # Replace with your desired topic

    MQTT_USERNAME = "admin"
    MQTT_PASSWORD = "rabbITMQ"

    # Create an instance of the MQTT client and connect to the broker
    mqtt_client = MQTTClient(
        MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_TOPIC
    )
    mqtt_client.connect(MQTT_KEEPALIVE_INTERVAL)

    # Create a Publisher instance and publish data
    publisher = Publisher(mqtt_client)

    try:
        publisher.publish_data(N=100)
        mqtt_client.client.loop_forever()

    except KeyboardInterrupt:
        mqtt_client.client.disconnect()
