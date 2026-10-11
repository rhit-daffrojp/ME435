import plateloader

def main():
    print("Serial Menu")
    # loader = plateloader.PlateLoader("/dev/tty/USB0")
    loader = plateloader.PlateLoader()
    loader.connect()
    print("0. Exit")
    print("1. RESET")
    print("2. X-AXIS")
    print("3. GRIPPER")
    print("4. Z-AXIS")
    print("5. MOVE")
    print("6. Status")
    while True:
        selection = int(input("Selection: "))
        if selection == 0:
            break
        elif selection == 1:
            response = loader.send_command("RESET")
            print(response)
        elif selection == 2:
            print("X-Axis Menu")
            print("0. Back to Main Menu")
            print("1. X-AXIS 1")
            print("2. X-AXIS 2")
            print("3. X-AXIS 3")
            print("4. X-AXIS 4")
            print("5. X-AXIS 5")
            selection = int(input("Selection: "))
            if selection == 0:
                continue
            elif selection == 1:
                response = loader.send_command("X-AXIS 1")
                print(response)
            elif selection == 2:
                response = loader.send_command("X-AXIS 2")
                print(response)
            elif selection == 3:
                response = loader.send_command("X-AXIS 3")
                print(response)
            elif selection == 4:
                response = loader.send_command("X-AXIS 4")
                print(response)
            elif selection == 5:
                response = loader.send_command("X-AXIS 5")
                print(response)
        elif selection == 3:
            print("Gripper Menu")
            print("0. Back to Main Menu")
            print("1. GRIPPER OPEN")
            print("2. GRIPPER CLOSE")
            selection = int(input("Selection: "))
            if selection == 0:
                continue
            elif selection == 1:
                response = loader.send_command("GRIPPER OPEN")
                print(response)
            elif selection == 2:
                response = loader.send_command("GRIPPER CLOSE")
                print(response)
        elif selection == 4:
            print("Z-Axis Menu")
            print("0. Back to Main Menu")
            print("1. Z-AXIS EXTEND")
            print("2. Z-AXIS RETRACT")
            selection = int(input("Selection: "))
            if selection == 0:
                continue
            elif selection == 1:
                response = loader.send_command("Z-AXIS EXTEND")
                print(response)
            elif selection == 2:
                response = loader.send_command("Z-AXIS RETRACT")
                print(response)
        elif selection == 5:
            print("Move: ")
            in1 = int(input("From: "))
            in2 = int(input("To: "))
            response = loader.send_command(f"MOVE {in1} {in2}")
            print(response)
        elif selection == 6:
            response = loader.send_command("LOADER_STATUS")
            print(response)
        

    
    
    
    loader.disconnect()
    print("Goodbye")




main()
