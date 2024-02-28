import paho.mqtt.client as mqtt
from .models import MqttMessage

class MqttClient:
    def __init__(self, broker_address, port=1883):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker_address, port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe("esp32")

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload}")

        # Save the message to the database
        MqttMessage.objects.create(topic=msg.topic, message=msg.payload.decode('utf-8'))

    def publish(self, topic, message):
        self.client.publish(topic, message)

mqtt_client = MqttClient("mqtt.eclipse.org")  # Use your MQTT broker address
