import motor
import time

class DriveSystem:
    def __init__(self):
        self.car = motor.OrdinaryCar()

    def scale_speed(self, speed):
        """ Returns a duty from 0 to 4095 based on given speed """
        return int(speed / 100 * 4095)

    def set_speeds(self, lf, lr, rf, rr):
        """ Pass in four speeds each -100 to 100 to set the wheel duty cycle """
        
        self.car.set_motor_model(self.scale_speed(lf),
                                 self.scale_speed(lr),
                                 self.scale_speed(rf),
                                 self.scale_speed(rr))

    def go(self, left_wheel_speed, right_wheel_speed):
        """ Speeds as integers from -100 to 100. """
        self.set_speeds(left_wheel_speed, left_wheel_speed, right_wheel_speed, right_wheel_speed)

    def stop(self):
        self.set_speeds(0, 0, 0, 0)

    def go_straight_for_seconds(self, seconds, speed):
        self.go(speed, speed)
        time.sleep(seconds)
        self.stop()

    def go_straight_for_inches(self, inches, speed):
        m = 0.7
        b = 0
        inches_per_sec = speed * m + b
        seconds = inches/inches_per_sec
        self.go_straight_for_seconds(seconds, speed)

    def spin_in_place_for_seconds(self, seconds, speed):
        self.set_speeds(-speed, -speed, speed, speed)
        time.sleep(seconds)
        self.stop()

    def spin_in_place_for_degrees(self, degrees, speed):
            m = 7.5
            b = 0
            deg_per_sec = speed * m + b
            seconds = degrees/deg_per_sec
            self.spin_in_place_for_seconds(seconds, speed)

    def draw_polygon(self, speed, sides, inches):
        degrees = 180-((180*(sides - 2))/sides)
        print(degrees)
        for i in range(sides):
            self.go_straight_for_inches(inches, speed)
            time.sleep(0.3)
            self.spin_in_place_for_degrees(degrees, speed)
            time.sleep(0.3)

