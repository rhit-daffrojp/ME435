import serial
import time

print("Learning Pyserial") # with pi400

ser = serial.Serial(port='/dev/ttyACM0', baudrate = 19200, timeout=10)  # open serial port
time.sleep(2.0) # Necessary sometimes. :)


#ser.open()     # Not necessary

ser.reset_input_buffer()  # flush input buffer, discarding all its contents
message = "RESET"
print(message)
message_bytes = (message + '\n').encode()  # convert to bytes
print(message_bytes)

ser.write(message_bytes)  # write a string

response_bytes = ser.readline()
print(response_bytes)
response = response_bytes.decode().strip()
print(response)


ser.close()  # close serial port