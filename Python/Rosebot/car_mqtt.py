# import gpiozero as gz
import mqtt_helper as mh
from rosebot import Rosebot
# import signal
import time
import datetime

# Can also use this code for Exam 3 and Lab 6

class App:

    def __init__(self):

        self.robot = Rosebot()
        self.is_streaming = True # As a temp test, normally False
        self.mode = "none"

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
        if message_type == "beep":
            self.robot.buzzer.beep(on_time=0.1, off_time=0.3, n=2)

def main():
    print("Car MQTT")
    app = App()
    last_time_sent_s = 0


    try:
        while True:

            right_now = datetime.datetime.now()
            current_time_s = right_now.timestamp()
            
            # Strategy is to look at the clock, if 2 seconds have passed do something.
            if app.is_streaming and current_time_s > last_time_sent_s + 2.0:
                last_time_sent_s = current_time_s
                app.mqtt_client.send_message("line_sensor_reading", {
                    "timestamp": right_now.strftime("%m/%d/%Y  %H:%M:%S"),
                    "left:": app.robot.line_sensors.get_left(),
                    "middle:": app.robot.line_sensors.get_middle(),
                    "right:": app.robot.line_sensors.get_right()
                })

        # signal.pause() # Keep the program alive but does nothing.
    except KeyboardInterrupt:
        print("Goodbye!")
        app.robot.drive_system.stop()
        app.mqtt_client.close()
main()
