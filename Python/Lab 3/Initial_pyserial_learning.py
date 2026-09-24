import serial

print("Learning Pyserial")

ser = serial.Serial(port='/dev/ttyACM0', baudrate = 19200, timeout=10)  # open serial port
#ser.open()
while not ser.is_open:
    print("Opening...")

# TODO: Use the serial object



ser.close()  # close serial port
