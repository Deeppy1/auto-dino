import serial
import time

# Step 1: Set up serial connection
# Replace 'COM3' with the correct port (e.g. '/dev/ttyUSB0' or '/dev/ttyACM0' on Linux/Mac)
ser = serial.Serial('COM3', 9600, timeout=1)

# Step 2: Give Arduino time to reset after opening serial port
time.sleep(2)

# Step 3: Send the message
message = "Hello Arduino!"
ser.write(message.encode())  # Convert string to bytes

# Optional: Close the serial connection
#ser.close()
