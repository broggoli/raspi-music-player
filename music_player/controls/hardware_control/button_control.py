from RPi import GPIO
from time import sleep
from datetime import datetime
from threading import Thread

class Button_Control(object):

    def __init__(self, buttonPin,
                callback,
                longClickCallback=False,
                bouncetime=200,
                pullDown=True):
        #Setting the button's GPIO pin number
        self.bttn = buttonPin
        self.threadCounter = 0
        self.pullDown = pullDown
        self.pressed = False

        #Setting the callbacks
        self.callback = callback
        self.bouncetime = bouncetime
        self.longClickCallback = longClickCallback
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
        GPIO.remove_event_detect(self.bttn)

    def _callback(self, pin):
        #print("callback from pin:", pin, GPIO.input(self.bttn))
        t = Thread(target=self.reportPress)
        t.start()

    def reportPress(self):
        inpt = GPIO.input(self.bttn)
        self.pressed = (self.pullDown and inpt == 1) or (not self.pullDown and inpt == 0)
        sleepTime = 0.05
        self.threadCounter += 1
        if self.threadCounter == 1 and self.pressed:
            while self.pressed:
                self.callback(self.bttn, True)
                sleep(sleepTime)
                inpt = GPIO.input(self.bttn)
                self.pressed = (self.pullDown and inpt == 1) or (not self.pullDown and inpt == 0)
            else:
                self.callback(self.bttn, False)
        self.threadCounter -= 1

    def long_sort_push_callback(self, longPushTime = 1):

        inpt = GPIO.input(self.bttn)
        self.pressed = (self.pullDown and inpt == 1) or (not self.pullDown and inpt == 0)
        sleepTime = 0.01
        longCallbackSleepTime = 0.2
        start = datetime.now()
        self.threadCounter += 1
        if self.threadCounter == 1 and self.pressed:
            if self.longClickCallback:
                while self.pressed:
                    timeElapsed = (datetime.now() - start).seconds
                    inpt = GPIO.input(self.bttn)
                    #print(timeElapsed, self.threadCounter, self.pressed)
                    if timeElapsed >= longPushTime:
                        self.callback(self.bttn, True)
                        sleep(longCallbackSleepTime)
                    else:
                        sleep(sleepTime)
                    self.pressed = (self.pullDown and inpt == 1) or (not self.pullDown and inpt == 0)
                else:
                    if timeElapsed < longPushTime:
                        self.callback(self.bttn, False)
            else:
                print("No long click callback defined!")
                self.callback(self.bttn, False)
        self.threadCounter -= 1
