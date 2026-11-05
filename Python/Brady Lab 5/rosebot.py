import gpiozero as gz
from rosebot_drive_system import DriveSystem
from rosebot_sensors import Ultrasonic
from rosebot_sensors import LineSensors


class Rosebot:
    def __init__(self):
        self.drive_system = DriveSystem()
        self.leds = None
        self.ultrasonic = Ultrasonic()
        self.line_sensors = LineSensors()
        self.servo_head = None # Might not need
        self.buzzer = gz.Buzzer(17)
        self.adc = None
