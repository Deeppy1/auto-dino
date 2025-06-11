import subprocess
import time
import serial
from PIL import Image
import os

# Constants
CACTUS_Y = 290
X_RANGE_START = 2700
X_RANGE_END = 3600
CACTUS_COLOR = "#acacac"
SCREENSHOT_PATH = '/home/Henry/Desktop/screen.png'

# Set up serial
try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    time.sleep(2)
except serial.SerialException as e:
    print(f"[ERROR] Could not open serial port: {e}")
    exit(1)

while True:
    try:
        # Take screenshot using grim
        subprocess.run(['grim', SCREENSHOT_PATH], check=True)

        # Wait a moment for the file to become readable
        while not os.path.exists(SCREENSHOT_PATH):
            time.sleep(0.01)

        image = Image.open(SCREENSHOT_PATH)

        # DINO detection
        pixel_rgb = image.getpixel((2626, 306))
        hex_color = '#{:02x}{:02x}{:02x}'.format(*pixel_rgb)
        jump = hex_color != CACTUS_COLOR
        print(f"[DINO] Pixel @ (2626, 306): {hex_color}, jump = {jump}")

        # DEAD detection
        pixel_rgb2 = image.getpixel((2880, 254))
        hex_color2 = '#{:02x}{:02x}{:02x}'.format(*pixel_rgb2)
        dead = hex_color2 == CACTUS_COLOR
        print(f"[DEAD] Pixel @ (2880, 254): {hex_color2}, dead = {dead}")

        # CACTUS detection
        cactus = False
        for x in range(X_RANGE_START, X_RANGE_END + 1):
            pixel = image.getpixel((x, CACTUS_Y))
            hex_color_cactus = '#{:02x}{:02x}{:02x}'.format(*pixel)
            if hex_color_cactus == CACTUS_COLOR:
                print(f"[CACTUS] Detected at X={x}, HEX={hex_color_cactus}")
                cactus = True
                break

        # Decision
        print(f"[LOGIC] dead={dead}, jump={jump}, cactus={cactus}")
        if not dead and not jump and cactus:
            time.sleep(0.75)  # Wait for jump animation
            print(">>> Sending 'R' to Arduino for jump.")
            ser.write(b'R')  # Send single-character command for speed
            time.sleep(0.25)

        else:
            print(">>> No jump sent.")

        # Optional delay
        # time.sleep(0.1)

    except Exception as e:
        print(f"[ERROR] {e}")
        time.sleep(1)
