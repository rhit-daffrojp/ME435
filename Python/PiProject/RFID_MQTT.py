import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522, MFRC522
import mqtt_helper as mh
from RFID_Class import RFIDScanner

# 1. Initialize the scanner with your authorized card IDs
AUTHORIZED_IDS = [
    849516823339,
    # 319668552350 WRONG ONE
]

rfid = RFIDScanner(authorized_cards=AUTHORIZED_IDS, pin_rst=5)

print("System ready. Waiting for RFID scan...")

try:
    while True:
        # 2. Call the class method to wait for and check a card
        is_valid, card_id = rfid.scan_card()
        print(f"Scanned Card ID: {card_id}")

        if is_valid:
            print("Welcome!")
            # Add your other GPIO actions here (e.g., unlock door, turn on LED)
        else:
            print("Not recognized.")

        # Brief pause to prevent duplicate reads from one tap
        time.sleep(2)

except KeyboardInterrupt:
    print("\nShutting down...")

finally:
    # 3. Clean up GPIO pins once when the entire program exits
    rfid.cleanup()



class App:

    def __init__(self):

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/daffrojp/#",
                                 publish_topic_name="me435/daffrojp/to_computer")#,
                                # use_off_campus_broker=True)   #use_off_campus_broker = True
        self.mqtt_client.callback = self.mqtt_callback

    def mqtt_callback(self, message_type, message_payload):

        if message_type == "stop":
            self.robot.drive_system.set_speeds(0, 0, 0, 0)


def main():
    print("Pi Project")
    app = App()
    last_time_sent_s = 0

    # Talking to myself:
    time.sleep(2)
    # app.mqtt_client.send_message("is_streaming", True)

    try:
        while True:
            # Strategy figure it out.
            return

    except KeyboardInterrupt:
        print("Goodbye!")
        app.robot.drive_system.stop()
        app.mqtt_client.close()
main()