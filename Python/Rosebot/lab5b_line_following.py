from rosebot import Rosebot
import time

def main():
    print("Lab 5b Line Following")
    robot = Rosebot()
 
    try:
        while True:
            print(robot.ultrasonic.get_cm())
            print(robot.line_sensors.get_line_word())
            
            # Get ultrasonic
            # if distance < 20 cm
            #   stop robot
            # else
 
 
            #   Get the line sensor readings
            #   Adjest wheel speeds based on your strategy
 
            time.sleep(0.1)
 
    except KeyboardInterrupt:
        # Handle ctrl c to exit program cleanly.
        robot.drive_system.stop()
        print("Goodbye!")
 
 
main()
