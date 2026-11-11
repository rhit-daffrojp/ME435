import time
from gpiozero import OutputDevice



class LCD:

    def lcd_init(self):
        # Pin Mapping for Raspberry Pi 5 (using Broadcom BCM Pin Numbers)
        self.LCD_RS = OutputDevice(22)
        self.LCD_E  = OutputDevice(17)
        self.LCD_D4 = OutputDevice(25)
        self.LCD_D5 = OutputDevice(24)
        self.LCD_D6 = OutputDevice(23)
        self.LCD_D7 = OutputDevice(18)

        # LCD commands
        self.LCD_WIDTH = 16    # Characters per line
        self.LCD_CHR = True
        self.LCD_CMD = False

        # Timing constants
        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD) # 011000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = data, mode = True for character, False for command
        self.LCD_RS.value = mode # High / Low selection

        # High bits
        self.LCD_D4.value = bool(bits & 0x10)
        self.LCD_D5.value = bool(bits & 0x20)
        self.LCD_D6.value = bool(bits & 0x40)
        self.LCD_D7.value = bool(bits & 0x80)
        self.lcd_toggle_enable()

        # Low bits
        self.LCD_D4.value = bool(bits & 0x01)
        self.LCD_D5.value = bool(bits & 0x02)
        self.LCD_D6.value = bool(bits & 0x04)
        self.LCD_D7.value = bool(bits & 0x08)
        self.lcd_toggle_enable()

    def lcd_toggle_enable(self):
        # Toggle enable pin
        time.sleep(self.E_DELAY)
        self.LCD_E.value = True
        time.sleep(self.E_PULSE)
        self.LCD_E.value = False
        time.sleep(self.E_DELAY)

    def lcd_string(self, message, line):
        # Send string to display
        message = message.ljust(self.LCD_WIDTH, " ")
        self.lcd_byte(line, self.LCD_CMD)
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

if __name__ == '__main__':
    lcd = LCD()
    try:
        LCD.lcd_init()
        LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
        LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

        while True:
            # Write to top and bottom lines
            lcd.lcd_string("Raspberry Pi 5", LCD_LINE_1)
            lcd.lcd_string("16x2 LCD Alive!", LCD_LINE_2)
            time.sleep(3)
            
            lcd.lcd_string("Status: Running", LCD_LINE_1)
            lcd.lcd_string("No Blinka Needed", LCD_LINE_2)
            time.sleep(3)
            
    except KeyboardInterrupt:
        # Clean up screen on exit
        lcd.lcd_byte(0x01, False) 
