from rosebot import Rosebot
import time

def main():
    print("Lab 5b Line Following")
    robot = Rosebot()

    try:
        while True:
            last_pos = None

            if robot.ultrasonic.get_cm() < 20:
                robot.drive_system.stop()
            else:
                current_pos = robot.line_sensors.get_line_word()

                if current_pos == "WBW":
                    robot.drive_system.set_speeds(20, 20, 20, 20)
                elif current_pos[0] == "B":
                    robot.drive_system.set_speeds(0, 0, 20, 20)
                elif current_pos[2] == "B":
                    robot.drive_system.set_speeds(20, 20, 0, 0)
                elif current_pos == "WWW":
                    if last_pos == "BWW":
                        robot.drive_system.set_speeds(0, 0, 25, 25)
                    elif last_pos == "WWB":
                        robot.drive_system.set_speeds(25, 25, 0, 0)

                last_pos = current_pos
                # if robot.line_sensors.get_line_word() == "WBW":
                #     robot.drive_system.set_speeds(20, 20, 20, 20)
                # elif robot.line_sensors.get_line_word() == "BWW" or robot.line_sensors.get_line_word() == "BBW":
                #     robot.drive_system.set_speeds(0, 0, 20, 20)
                # elif robot.line_sensors.get_line_word() == "WWB" or robot.line_sensors.get_line_word() == "WBB":
                #     robot.drive_system.set_speeds(20, 20, 0, 0)
                # else:
                #     robot.drive_system.set_speeds(0, 0, 0, 0)
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Handle ctrl c to exit program cleanly.
        robot.drive_system.stop()
        print("Goodbye!")

# def follow_line(self, robot):
#     if robot.line_sensors.get_line_word() == "WBW":
#         robot.drive_system.set_speeds(30, 30, 30, 30)
#     elif robot.line_sensors.get_line_word() == "BWW":
#          robot.drive_system.set_speeds(0, 0, 30, 30)
#     elif robot.line_sensors.get_line_word() == "WWB":
#         robot.drive_system.set_speeds(30, 30, 0, 0)
#     else:
#         robot.drive_system.set_speeds(20, 20, 20, 20)


main()