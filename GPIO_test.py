from RPi import GPIO
from time import sleep
import os

GPIO.setmode(GPIO.BCM)
pin = 5
#The button needs a pull up resistor in order to not float
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:

        print(GPIO.input(pin))
        sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
