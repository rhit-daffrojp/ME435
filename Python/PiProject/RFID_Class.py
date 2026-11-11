import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522, MFRC522


class _CustomMFRC522(SimpleMFRC522):
    """Internal helper to override the default RST pin (GPIO 25)."""
    def __init__(self, pin_rst=5):
        self.READER = MFRC522(pin_rst=pin_rst)


class RFIDScanner:
    def __init__(self, authorized_cards=None, pin_rst=5):
        self.reader = _CustomMFRC522(pin_rst=pin_rst)
        self.authorized_cards = set(authorized_cards) if authorized_cards else set()

    def scan_card(self):
        """Waits for a card tap and returns a tuple: (is_authorized, card_id)."""
        card_id, _ = self.reader.read()
        is_authorized = card_id in self.authorized_cards
        return is_authorized, card_id

    def add_card(self, card_id):
        """Adds a new card ID to the authorized set."""
        self.authorized_cards.add(card_id)

    def cleanup(self):
        """Resets GPIO pins when shutting down."""
        GPIO.cleanup()

    def scan_card_nonblocking(self):
        card_id, _ = self.reader.read_no_block()   # (None, None) when no card present
        if card_id is None:
            return None, None
        return card_id in self.authorized_cards, card_id


# Optional: Only runs if you execute RFID_Scan.py directly for testing
if __name__ == "__main__":
    scanner = RFIDScanner(authorized_cards=[123456789012])
    try:
        print("Test mode: Tap a card...")
        authorized, cid = scanner.scan_card()
        print(f"Card ID: {cid} | Authorized: {authorized}")
    finally:
        scanner.cleanup()
