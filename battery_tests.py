from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
lowBatteryPin = 21
batPin = 20

GPIO.setup(lowBatteryPin, GPIO.IN)
GPIO.setup(batPin, GPIO.IN)

try:
    while(True):
        print(GPIO.input(batPin), GPIO.input(lowBatteryPin))
        sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()
