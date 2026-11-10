import mqtt_helper as mh
import signal
import time
from rosebot import Rosebot
import datetime

class App:

    def __init__(self):
        self.robot = Rosebot()
        self.is_streaming = False
        self.mode = "none"

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/mccreebs/#",
                                 publish_topic_name="me435/mccreebs/to_computer")
        self.mqtt_client.callback = self.mqtt_callback



    def mqtt_callback(self, message_type, message_payload):
        print("Received type: ", message_type)
        print("Received payload: ", message_payload)

        if message_type == "set_speeds":
            self.robot.drive_system.set_speeds(message_payload[0], message_payload[1], message_payload[2], message_payload[3])
        if message_type == "stop":
            self.robot.drive_system.set_speeds(0, 0, 0, 0)

        if message_type == "beep":
            self.robot.buzzer.beep(on_time = 0.1, off_time = 0.3, n=2)

        if message_type == "is_streaming":
            self.is_streaming = message_payload

        if message_type == "mode":
            self.mode = message_payload
            if self.mode == "drive_until_wall" or self.mode == "drive_until_line":
                self.robot.drive_system.go(20, 20)
            if self.mode == "none":
                self.robot.drive_system.stop()



def main():
    print("Car MQTT")
    app = App()
    last_time_sent_s = 0

    # Talking to myself
    time.sleep(1)
    # app.mqtt_client.send_message("is_streaming", True)
    # app.mqtt_client.send_message("mode", "drive_until_line")

    try:
        while True:
            right_now = datetime.datetime.now()
            current_time_s = right_now.timestamp()

            # Strategy is to look at the clock, if two seconds have passed, do something.
            if app.is_streaming and current_time_s > last_time_sent_s + 2.0:
                last_time_sent_s = current_time_s
                app.mqtt_client.send_message("line_sensor_readings", {
                    "timestamp": right_now.strftime("%m/%d/%Y | %H:%M:%S"),
                    "left": app.robot.line_sensors.get_left(),
                    "middle": app.robot.line_sensors.get_middle(),
                    "right": app.robot.line_sensors.get_right(),
                })


            if app.mode == "drive_until_wall":
                # Check for wall
                if app.robot.ultrasonic.get_cm() < 40:
                    app.robot.drive_system.stop()
                    app.robot.buzzer.beep(on_time=0.1, off_time=0.1, n=3)
                    app.mode = "none"
            
            if app.mode == "drive_until_line":
                # Check for wall
                if app.robot.line_sensors.get_line_word() != "WWW":
                    app.robot.drive_system.stop()
                    app.robot.buzzer.beep(on_time=0.1, off_time=0.1, n=2)
                    app.mode = "none"

            if app.mode == "line_following":

                last_pos = None

                if app.robot.ultrasonic.get_cm() < 20:
                    app.robot.drive_system.stop()
                else:
                    current_pos = app.robot.line_sensors.get_line_word()

                    if current_pos == "WBW":
                        app.robot.drive_system.set_speeds(20, 20, 20, 20)
                    elif current_pos[0] == "B":
                        app.robot.drive_system.set_speeds(0, 0, 20, 20)
                    elif current_pos[2] == "B":
                        app.robot.drive_system.set_speeds(20, 20, 0, 0)
                    elif current_pos == "WWW":
                        if last_pos == "BWW":
                            app.robot.drive_system.set_speeds(0, 0, 25, 25)
                        elif last_pos == "WWB":
                            app.robot.drive_system.set_speeds(25, 25, 0, 0)

                    last_pos = current_pos
                    

        # signal.pause() # Keep the program alive but does nothing.
    except KeyboardInterrupt:
        print("Goodbye")
        app.robot.drive_system.stop()
        app.mqtt_client.close()



main()