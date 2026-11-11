from LiquidCrystalDisplay import LCD
import mqtt_helper as mh
import signal
import time
import datetime

class App:

    def __init__(self):
        self.lcd = LCD()

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/mccreebs/#",
                                 publish_topic_name="me435/mccreebs/to_computer")
        self.mqtt_client.callback = self.mqtt_callback



    def mqtt_callback(self, message_type, message_payload):
        print("Received type: ", message_type)
        print("Received payload: ", message_payload)

        # if message_type == "left":
        #     if message_payload[0] == 1:
        #         self.robot.drive_system.set_speeds(message_payload[2], message_payload[2], 0, 0)
        #     elif message_payload[0] == 0:
        #         self.robot.drive_system.set_speeds(-message_payload[2], -message_payload[2], 0, 0) 
        #     time.sleep(message_payload[1])
        #     self.robot.drive_system.stop()     

       
def main():
    print("8-Ball MQTT")
    app = App()
    last_time_sent_s = 0

    try:
        while True:
            # right_now = datetime.datetime.now()
            # current_time_s = right_now.timestamp()

            # if current_time_s > last_time_sent_s + 2.0:
            #     last_time_sent_s = current_time_s
            #     app.mqtt_client.send_message("ultra", app.robot.ultrasonic.get_cm())
            

            signal.pause() # Keep the program alive but does nothing.
    except KeyboardInterrupt:
        print("Goodbye")
        app.lcd.lcd_byte(0x01, False) 



main()
