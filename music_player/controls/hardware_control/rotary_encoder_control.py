from RPi import GPIO

class Rotary_Encoder_Control(object):
    """
        Rotary_encoder is a class to control a rotary encoder
        for example a volume control.
        Use for rotary encoder KY040.

        Much of this code was 'inspired' by the code of martinohanlon on github:
        https://github.com/martinohanlon/KY040/blob/master/ky040/KY040.py
    """

    def __init__(self, clockPin, dataPin,
                rotaryCallback,
                rotaryBouncetime=50):
        #These two GPIO Pins encodes the rotation
        self.clk = clockPin
        self.dt = dataPin

        #Setting the callbacks
        #Saving the callback functions that are called when an even occurs
        self.rotaryCallback = rotaryCallback
        #Setting the bounce time
        self.rotaryBouncetime = rotaryBouncetime

        #setting the GPIO pins up
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.dt, GPIO.IN)

        #setting the clk state for determining the direction of the turn
        self.clkLastState = GPIO.input(self.dt)

    def start(self):
        #Adds event detectors to the clock and the switch pin
        GPIO.add_event_detect(self.clk, GPIO.FALLING, callback=self._clockCallback, bouncetime=self.rotaryBouncetime)

    def stop(self):
        #removes the event detectors
        GPIO.remove_event_detect(self.clk)

    def _clockCallback(self, pinNr):
        #calls the callback function with the direction encoded as the question:
        # is the rotation clockwise? -> True or False
        clkState = GPIO.input(self.clk)
        if clkState == 0:
            if GPIO.input(self.dt) != clkState:
                self.rotaryCallback(False)
            else:
                self.rotaryCallback(True)
