from RPi import GPIO
from time import sleep

class Button_Control(object):

    def __init__(self, buttonPin,
                callback,
                bouncetime=200,
                pullDown=True):
        #Setting the button's GPIO pin number
        self.bttn = buttonPin
        self.pullDown = pullDown

        #Setting the callbacks
        self.callback = callback
        self.bouncetime = bouncetime
        #setting the GPIO pins up
        GPIO.setmode(GPIO.BCM)
        if self.pullDown:
            upOrDown = GPIO.PUD_DOWN
        else:
            upOrDown = GPIO.PUD_UP
        #The button needs a pull up or down resistor in order to not float
        GPIO.setup(self.bttn, GPIO.IN, pull_up_down=upOrDown)

    def start(self):
        #Adds event detectors to the button pin
        if self.pullDown:
            detect = GPIO.RISING
        else:
            detect = GPIO.FALLING

        GPIO.add_event_detect(self.bttn, detect, callback=self._callback, bouncetime=self.bouncetime)

    def stop(self):
        #removes the event detector
        GPIO.remove_event_detect(self.bttn)

    def _callback(self, pin):
        #print("callback from pin:", pin, GPIO.input(self.bttn))
        inpt = GPIO.input(self.bttn)
        if (self.pullDown and inpt == 1) or (not self.pullDown and inpt == 0):
            self.callback()
