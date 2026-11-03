# import gpiozero as gz
import mqtt_helper as mh
from rosebot import Rosebot
import signal
import time

# Can also use this code for Exam 3 and Lab 6

class App:

    def __init__(self):

        self.robot = Rosebot()
        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/daffrojp/#",
                                 publish_topic_name="me435/daffrojp/to_computer")
        self.mqtt_client.callback = self.mqtt_callback

    def mqtt_callback(self, message_type, message_payload):
        print("Received type: ", message_type)
        print("Received payload: ", message_payload)

        if message_type == "set_speeds":
            self.robot.drive_system.set_speeds(message_payload[0], message_payload[1], message_payload[2], message_payload[3])
        if message_type == "stop":
            self.robot.drive_system.set_speeds(0, 0, 0, 0)

def main():
    print("Car MQTT")
    app = App()
    try:
        while True:
            # Send test messages!
            app.mqtt_client.send_message("set_speeds", [40, 40, 40, 40])
            time.sleep(1)
            app.mqtt_client.send_message("stop")
            time.sleep(1)

        # signal.pause() # Keep the program alive but does nothing.
    except KeyboardInterrupt:
        print("Goodbye!")
        app.robot.drive_system.stop()
        app.mqtt_client.close()
main()
