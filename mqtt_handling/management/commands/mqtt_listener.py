import time
import threading
from django.core.management.base import BaseCommand
from mqtt_handling.mqtt_utils import MqttClient  # Adjust the import path as needed


class Command(BaseCommand):
    help = 'Run MQTT listener in the background'

    def handle(self, *args, **options):
        mqtt_client = MqttClient("192.168.1.1")  # Use your MQTT broker address

        def run_mqtt_listener():
            mqtt_client.client.loop_forever()

        thread = threading.Thread(target=run_mqtt_listener)
        thread.daemon = True
        thread.start()

        try:
            # Keep the main thread alive
            while True:
                time.sleep(10)  # Adjust the sleep interval as needed
        except KeyboardInterrupt:
            mqtt_client.client.disconnect()
