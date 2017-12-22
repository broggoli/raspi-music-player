from RPi import GPIO
from time import sleep
import alsaaudio

class Rotary_Encoder(object):
    """
        Rotary_encoder is a class to control a rotary encoder
        for example a volume control.
        Use for rotary encoder KY040.

        Much of this code was 'inspired' by the code of martinohanlon on github:
        https://github.com/martinohanlon/KY040/blob/master/ky040/KY040.py
    """

    def __init__(self, clockPin, dataPin,
                rotaryCallback,
                rotaryBouncetime=250):
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
        GPIO.setup(self.clk, GPIO.IN)
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
        if GPIO.input(self.clk) == 0:
            data = GPIO.input(self.dt)
            if data == 1:
                self.rotaryCallback(False)
            else:
                self.rotaryCallback(True)

class Volume_Control(object):
    """
        A volume control class to easily handle a rotary encoder

        Arguments:
            volume: the inital volume. In order to reset the volume before shutting of the device
            min- & max_volume: pretty self explanatory
    """

    def __init__(self, initial_volume, clockPin, dataPin, min_volume=0, max_volume=100):
        self.volume = initial_volume
        self.minMaxVol = (min_volume, max_volume)
        self.RE = Rotary_Encoder(clockPin, dataPin, self.adjust_volume_variable)

        #self.volume_mixer = alsaaudio.Mixer(alsaaudio.mixers[0])

    def start(self):
        self.RE.start()

    def adjust_volume_variable(self, clockwise, adjustment_step = 1):
        #If the direction is clockwise -> True -> increase Volume, else decrease Volume

        if clockwise:
            self.volume += adjustment_step
        else:
            self.volume -= adjustment_step

        #keeping the volume in between min- and max_volume
        self.volume = max(self.minMaxVol[0], self.volume)
        self.volume = min(self.volume, self.minMaxVol[1])

        #Change the systems Volume
        #self.volume_mixer.setvolume(self.volume)
        print("Set volume to:", self.volume)

        return True
