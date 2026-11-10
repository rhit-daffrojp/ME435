import mqtt_helper as mh
from rosebot import Rosebot
import time
import datetime

class App:

    def __init__(self):

        self.robot = Rosebot()
        self.is_streaming = True

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/daffrojp/#",
                                 publish_topic_name="me435/daffrojp/to_computer")#,
                                # use_off_campus_broker=True)   #use_off_campus_broker = True
        self.mqtt_client.callback = self.mqtt_callback

    def mqtt_callback(self, message_type, message_payload):

        if message_type == "stop":
            self.robot.drive_system.set_speeds(0, 0, 0, 0)

        if message_type == "left":
            if message_payload[0] == 0:
                message_payload[2] = -message_payload[2]
            self.robot.drive_system.set_speeds(message_payload[2], message_payload[2], 0, 0)
            time.sleep(message_payload[1])
            self.robot.drive_system.set_speeds(0, 0, 0, 0)

        if message_type == "right":
            if message_payload[0] == 0:
                message_payload[2] = -message_payload[2]
            self.robot.drive_system.set_speeds(0, 0, message_payload[2], message_payload[2])
            time.sleep(message_payload[1])
            self.robot.drive_system.set_speeds(0, 0, 0, 0)
        
        if message_type == "both":
            if message_payload[0] == 0:
                message_payload[2] = -message_payload[2]
                message_payload[3] = -message_payload[3]
            self.robot.drive_system.set_speeds(message_payload[2], message_payload[2], message_payload[3], message_payload[3])
            time.sleep(message_payload[1])
            self.robot.drive_system.set_speeds(0, 0, 0, 0)

def main():
    print("Car MQTT")
    app = App()
    last_time_sent_s = 0

    # Talking to myself:
    time.sleep(2)
    # app.mqtt_client.send_message("is_streaming", True)

    try:
        while True:

            right_now = datetime.datetime.now()
            current_time_s = right_now.timestamp()
            
            # Strategy is to look at the clock, if 2 seconds have passed do something.
            if app.is_streaming and current_time_s > last_time_sent_s + 2.0:
                last_time_sent_s = current_time_s
                app.mqtt_client.send_message("ultra", app.robot.ultrasonic.get_cm())

    except KeyboardInterrupt:
        print("Goodbye!")
        app.robot.drive_system.stop()
        app.mqtt_client.close()
main()