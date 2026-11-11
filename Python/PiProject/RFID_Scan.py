import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522, MFRC522

# Custom class to override the default RST pin (GPIO 25) with your free GPIO 5
class CustomRFID(SimpleMFRC522):
    def __init__(self):
        self.READER = MFRC522(pin_rst=5)

reader = CustomRFID()

# Replace these sample numbers with the actual IDs of your authorized cards
AUTHORIZED_CARDS = [
    123456789012,
    987654321098
]

print("RFID Reader Ready. Hold a card near the reader (Press Ctrl+C to exit)...")

try:
    while True:
        # Wait for a card to be scanned
        card_id, text = reader.read()
        print(f"Scanned Card ID: {card_id}")

        # Check if the scanned ID is in your authorized list
        if card_id in AUTHORIZED_CARDS:
            print("Welcome!")
        else:
            print("Not recognized.")

        # Pause briefly so a single tap doesn't trigger multiple times
        time.sleep(2)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    # Safely reset GPIO pins on exit
    GPIO.cleanup()
