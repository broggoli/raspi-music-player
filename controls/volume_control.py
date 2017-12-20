from RPi import GPIO
from time import sleep

class Rotary_encoder(object):
    """
        Rotary_encoder is a class to control a rotary encoder
        for example a volume control.
    """

    def __init__(self, clkGPIOpin, dtGPIOpin, swGPIOpin):
        #encodes the rotation
        self.clk = clkGPIOpin
        self.dt = dtGPIOpin

        #Checks for cklick events
        self.sw = swGPIOpin

        #set the GPIO pins up
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.clkLastState = GPIO.input(self.dt)

    def check_direction(self):
        """ returns 0 if nothing happened, 1 if clockwise turn, -1 if counterclockwise"""
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)
        #set the neutral direction to 0
        direction = 0

        if clkState != self.clkLastState:

            print("SW: ", GPIO.input(self.sw))
            print("DT: ", GPIO.input(self.dt))
            print("CLK: ", GPIO.input(self.clk))

            # if there was an event set the direction to the corresponding value
            if dtState != clkState:
                    direction = 1
            else:
                    direction = -1

        self.clkLastState = clkState
        return direction

class Volume_control(object):
    """
        A volume control class to easily handle a rotary encoder

        Arguments:
            volume: the inital volume. In order to reset the volume before shutting of the device
            min- & max_volume: pretty self explanatory
    """

    def __init__(self, volume, min_volume=0, max_volume=100):
        self.vol = volume
        self.minMaxVol = (min_volume, max_volume)
        self.RE = Rotary_encoder(clkGPIOpin=27, dtGPIOpin=18, swGPIOpin=7)

    def check_volume(self):
        #If the direction is to the right: 1, left: -1, center: 0, adjust it

        self.vol += self.RE.check_direction()


        #keeping the volume in between min- and max_volume
        self.vol = max(self.minMaxVol[0], self.vol)
        self.vol = min(self.vol, self.minMaxVol[1])

        return self.vol
