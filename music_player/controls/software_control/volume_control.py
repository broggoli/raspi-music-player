import alsaaudio

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

        #self.volume_mixer = alsaaudio.Mixer(alsaaudio.mixers[0])

    def change_volume(self, clockwise, adjustment_step = 5):
        #If the direction is clockwise -> True -> increase Volume, else decrease Volume

        if clockwise:
            self.volume += adjustment_step
        else:
            self.volume -= adjustment_step
        self.volume = int(self.volume)
        #keeping the volume in between min- and max_volume
        self.volume = max(self.minMaxVol[0], self.volume)
        self.volume = min(self.volume, self.minMaxVol[1])

        #Change the systems Volume
        #self.volume_mixer.setvolume(self.volume)
        print("[]"*(int(self.volume/2)))

        return True
