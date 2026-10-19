import gpiozero as gz
import time
import signal

def basic_on_off():
    print("Basic On / Off")
    green_led = gz.DigitalOutputDevice(18)
    green_led.on()
    time.sleep(3)
    green_led.off()

def fancy_leds():
    print("Fancy LEDs")
    red_led = gz.LED(14)
    yellow_led = gz.LED(15)
    green_led = gz.LED(18)

    # yellow_led.blink(on_time=2, off_time=0.1, n=3, background=False)
    red_led.blink(on_time=2, off_time=0.1)
    time.sleep(0.1)
    yellow_led.blink(on_time=2, off_time=0.1)
    time.sleep(0.1)
    green_led.blink(on_time=2, off_time=0.1)
    signal.pause()  # Wait for a signal (like Ctrl+C) to exit the program


def led_board():
    print("LED Board")

    # Construct it
    led_board = gz.LEDBoard(14, 15, 18, pwm=True)  # Red, Yellow, Green

    # Make a loop that runs five times
    for i in range(5):
        led_board.on()
        time.sleep(1)
        led_board.off()
        time.sleep(1)
        led_board.value = (1, 0, 1)  # Turn on the red and green LEDs
        time.sleep(1)
        led_board.value = (0, 0, 0)  # Turn off the red and green LEDs
        time.sleep(1)
        led_board.value = (0, 0.5, 0)  # Set the yellow LED to half brightness
        time.sleep(1)
        led_board.value = (0, 0, 0)  # Turn off the yellow LED
        time.sleep(1)


    

def main():
    print("Leds")
    # basic_on_off()
    # fancy_leds()
    led_board()



main()
