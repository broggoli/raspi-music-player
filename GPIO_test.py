from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
pin = 16
#The button needs a pull up resistor in order to not float
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while(True):
        print(GPIO.input(pin))
        sleep(0.05)

except KeyboardInterrupt:
    GPIO.cleanup()
