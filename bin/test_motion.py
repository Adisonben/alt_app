import RPi.GPIO as GPIO
import time

PIR_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

print("กำลังเริ่มต้นเซ็นเซอร์...")

time.sleep(2)

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Motion Detected!")
        else:
            print("No Motion")

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()