import motor
import time

class DriveSystem:

    def __init__ (self):
        self.car = motor.OrdinaryCar()

    def scale_speed(self, speed):
        """ Returns an int duty of 0 to 4095 (or 0 to -4095) for a given speed of. """
        return int(speed / 100 * 4095)

    def set_speeds(self, left_front, left_rear, right_front, right_rear):
        """Pass in 4 speeds as integers between -100 and 100.  Negative means go backwards."""
        self.car.set_motor_model(self.scale_speed(left_front),
                                 self.scale_speed(left_rear),
                                 self.scale_speed(right_front),
                                 self.scale_speed(right_rear))

    def go(self, left_wheel_speed, right_wheel_speed):
        """Speeds as integers between -100 and 100.  Negative means go backwards."""
        self.set_speeds(left_wheel_speed, left_wheel_speed, right_wheel_speed, right_wheel_speed)

    def stop(self):
        self.set_speeds(0, 0, 0, 0)
    
    def go_straight_for_seconds(self, seconds, speed):
        self.go(speed, speed)
        time.sleep(seconds)
        self.stop()
        