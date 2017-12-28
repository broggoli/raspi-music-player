import alsaaudio
from datetime import datetime
import time
from threading import Thread

class Volume_Control(object):
    """
        A volume control class to easily handle a rotary encoder

        Arguments:
            volume: the inital volume. In order to reset the volume before shutting of the device
            min- & max_volume: pretty self explanatory
    """

    def __init__(self, initial_volume, min_volume=0, max_volume=100):
        self.volume = initial_volume
        self.minMaxVol = (min_volume, max_volume)
        #only update the display after there was no action for given amount of seconds
        self.cooldownTime = 0.5
        self.recentlyCalled = False
        self.lastCalled = datetime.now()
        """
        print(alsaaudio.mixers)
        self.volume_mixer = alsaaudio.Mixer(alsaaudio.mixers[0])
        """
    def change_volume(self, clockwise, callback, adjustment_step = 5):
        #If the direction is clockwise -> True -> increase Volume, else decrease Volume

        self.callback = callback
        if clockwise:
            vol = self.volume + adjustment_step
        else:
            vol = self.volume - adjustment_step
        temp_vol = int(vol)
        #keeping the volume in between min- and max_volume
        vol = max(self.minMaxVol[0], vol)
        vol = min(vol, self.minMaxVol[1])

        #If the volume is between 100 an 0 change it
        if temp_vol == vol:
            #Change the system's Volume
            #print("[]"*(int(self.volume/2)))
            self.set_volume(vol)
            return True

    def exec_if_time_passed(self):
        """ This function is necessary because the Display has such a low refresh rate."""
        time.sleep(self.cooldownTime)
        #print((datetime.now() - self.lastCalled).microseconds)
        if((datetime.now() - self.lastCalled).microseconds >= self.cooldownTime * 1000000):
            self.callback(self.volume)

    def set_volume(self, vol, callback=None):
        if callback:
            self.callback = callback
        print("setting volume!")
        self.volume = vol

        self.lastCalled = datetime.now()
        t = Thread(target=self.exec_if_time_passed)
        t.start()
        #self.volume_mixer.setvolume(self.volume)
