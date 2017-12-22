from RPi import GPIO

class Button_Control(object):

    def __init__(self, buttonPin,
                callback,
                bouncetime=300):
        #Setting the button's GPIO pin number
        self.bttn = buttonPin

        #Setting the callbacks
        self.callback = callback
        self.bouncetime = bouncetime
        #setting the GPIO pins up
        GPIO.setmode(GPIO.BCM)
        #The button needs a pull up resistor in order to not float
        GPIO.setup(self.bttn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def start(self):
        #Adds event detectors to the button pin
        GPIO.add_event_detect(self.bttn, GPIO.FALLING, callback=self._callback, bouncetime=self.bouncetime)

    def stop(self):
        #removes the event detector
        GPIO.remove_event_detect(self.button)

    def _callback(self):
        if GPIO.input(self.bttn) == 0:
            self.callback()
