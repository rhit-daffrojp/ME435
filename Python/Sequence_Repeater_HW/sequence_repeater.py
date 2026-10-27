import gpiozero as gz
import time
import signal

def on(pin_num):
    if pin_num == 14:
        led_board.value = (1, 0, 0)  # Turn on the red LED
    elif pin_num == 15:
        led_board.value = (0, 1, 0)  # Turn on the yellow LED
    elif pin_num == 18:
        led_board.value = (0, 0, 1)  # Turn on the green LED

def off(pin_num):
    led_board.value = (0, 0, 0)  # Turn off all LEDs

def store(pin_num):
    seq.append(pin_num)
    on(pin_num)

def play(seq):
    for pin in seq:
        on(pin)
        time.sleep(0.5)
        off(pin)
        time.sleep(0.1)
    seq.clear()

led_board = gz.LEDBoard(14, 15, 18, pwm=True)  # Red, Yellow, Green   
play_button = gz.Button(25)
red_button = gz.Button(22)
yellow_button = gz.Button(23)
green_button = gz.Button(24)
seq = []

def main():
    print("Sequence Repeater Homework")

    red_button.when_pressed = lambda: store(14)
    yellow_button.when_pressed = lambda: store(15)
    green_button.when_pressed = lambda: store(18)

    red_button.when_released = lambda: off(14)
    yellow_button.when_released = lambda: off(15)
    green_button.when_released = lambda: off(18)

    play_button.when_pressed = lambda: play(seq)

    signal.pause()


main()
