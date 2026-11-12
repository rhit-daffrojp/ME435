import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522, MFRC522
import mqtt_helper as mh
from RFID_Class import RFIDScanner
from gpiozero import OutputDevice
from LiquidCrystalDisplay import LCD
import random

class App:

    def __init__(self):
        self.mode = "none"

        self.mqtt_client = mh.MqttClient()
        self.mqtt_client.connect(subscription_topic_name="me435/daffrojp/#",
                                 publish_topic_name="me435/daffrojp/to_computer")#,
                                # use_off_campus_broker=True)   #use_off_campus_broker = True
        self.mqtt_client.callback = self.mqtt_callback
         

    def mqtt_callback(self, message_type, message_payload):
        if message_type == "button":
            print(self.mode)
            if message_payload == True:
                print("Button pressed")
                self.mode = "button"
                print(self.mode)


def main():
    print("Pi Project")
    app = App()

    # 1. Initialize the scanner with your authorized card IDs
    AUTHORIZED_IDS = [849516823339]

    rfid = RFIDScanner(authorized_cards=AUTHORIZED_IDS, pin_rst=5)

    print("System ready. Waiting for RFID scan...")
    lcd = LCD()

    try:
        lcd.lcd_init()
        LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

        # Write to top and bottom lines
        lcd.lcd_string("Scan Card", LCD_LINE_1)
        lcd.lcd_string(" ", LCD_LINE_2)
        time.sleep(3)

        state = "waiting_for_card"   # waiting_for_card -> waiting_for_button -> (thinking) -> waiting_for_card

        while True:
            if state == "waiting_for_card":
                is_valid, card_id = rfid.scan_card_nonblocking()
                lcd.lcd_string("Scan Card", LCD_LINE_1)
                lcd.lcd_string(" ", LCD_LINE_2)
                if card_id is not None:
                    print(f"Scanned Card ID: {card_id}")
                    if is_valid:
                        lcd.lcd_string("Payment Received", LCD_LINE_1)
                        lcd.lcd_string("Tap Button", LCD_LINE_2)
                        app.mqtt_client.send_message("payment", True)
                        app.mode = "none"            # clear any stale button press
                        state = "waiting_for_button"
                    else:
                        lcd.lcd_string("Payment Invalid", LCD_LINE_1)
                        lcd.lcd_string("Try again", LCD_LINE_2)
                        app.mqtt_client.send_message("payment", False)
                        time.sleep(5)
                        app.mqtt_client.send_message("reset")

            elif state == "waiting_for_button":
                if app.mode == "button":
                    for _ in range(4):
                        lcd.lcd_string("Thinking", LCD_LINE_1)
                        lcd.lcd_string(" ", LCD_LINE_2)
                        time.sleep(0.25)
                        lcd.lcd_string("Thinking.", LCD_LINE_1)
                        time.sleep(0.25)
                        lcd.lcd_string("Thinking..", LCD_LINE_1)
                        time.sleep(0.25)
                        lcd.lcd_string("Thinking...", LCD_LINE_1)
                        time.sleep(0.25)


                    fortune1 = lambda n: {
                        1: "We get an A",
                        2: "Inshallah Winter",
                        3: "Is this quarter",
                        4: "Shoot your shot",
                        5: "Closed mouths",
                        6: "Yes",
                        7: "No",
                        8: "Homework will be",
                        9: "This is the best",
                        10: "Brady McCreamy"
                    }.get(n, "Unknown fortune.")
                    fortune2 = lambda n: {
                        1: "on this project.",
                        2: "Quarter is ours.",
                        3: "over yet? please.",
                        4: "cuzzo.",
                        5: "don't get fed.",
                        6: " ",
                        7: "",
                        8: "done sometime",
                        9: "project ever.",
                        10: "is the goat."
                        }.get(n, "Unknown fortune.")
                    n = random.randint(1, 10)   # inclusive: can return 1 through 10
                    
                    lcd.lcd_string(fortune1(n), LCD_LINE_1)
                    lcd.lcd_string(fortune2(n), LCD_LINE_2)
                    time.sleep(10)
                    app.mqtt_client.send_message("reset")
                    app.mode = "none"
                    state = "waiting_for_card"
                    is_valid = False

            time.sleep(0.05)   # keep the loop from spinning at 100% CPU

    except KeyboardInterrupt:
        print("\nShutting down...")
        # Clean up screen on exit
        lcd.lcd_byte(0x01, False) 

    finally:
        # 3. Clean up GPIO pins once when the entire program exits
        rfid.cleanup()

main()
