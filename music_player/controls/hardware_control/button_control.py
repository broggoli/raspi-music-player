from RPi import GPIO
from time import sleep
from datetime import datetime
from threading import Thread

class Button_Control(object):

    def __init__(self, buttonPin,
                shortClickCallback,
                longClickCallback = None,
                bouncetime=200,
                pullDown=True):
        #Setting the button's GPIO pin number
        self.bttn = buttonPin
        self.threadCounter = 0
        self.pullDown = pullDown

        #Setting the callbacks
        self.shortClickCallback = shortClickCallback
        self.longClickCallback = longClickCallback
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
        t = Thread(target=self.determin_push_length)
        t.start()

    def determin_push_length(self, longPushTime = 1):

        inpt = GPIO.input(self.bttn)
        pressed = (self.pullDown and inpt == 1) or (not self.pullDown and inpt == 0)
        sleepTime = 0.02
        start = datetime.now()
        self.threadCounter += 1
        if self.threadCounter == 1 and pressed:
            if self.longClickCallback:
                while pressed:
                    sleep(sleepTime)
                    timeElapsed = (datetime.now() - start).seconds
                    inpt = GPIO.input(self.bttn)
                    #print(timeElapsed, self.threadCounter, pressed)
                    if timeElapsed >= longPushTime:
                            self.longClickCallback()
                            sleep(0.5)
                    pressed = (self.pullDown and inpt == 1) or (not self.pullDown and inpt == 0)
                else:
                    if timeElapsed < longPushTime:
                        self.shortClickCallback()
            else:
                print("No long click callback defined!")
                self.shortClickCallback()
        self.threadCounter -= 1
