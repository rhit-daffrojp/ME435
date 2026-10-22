import motor

class DriveSystem:

    def __init__ (self):
        self.car = motor.OrdinaryCar()

    def go(self, left_wheel_speed, right_wheel_speed):
        """Speeds as integers between -100 and 100.  Negative means go backwards."""
        pass

    def stop(self):
        pass
    