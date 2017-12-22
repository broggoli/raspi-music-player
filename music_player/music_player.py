""" Music player app"""

from time import sleep
from RPi import GPIO

from controls.volume_control import Volume_control
from controls.button_interface import Button_interface

class Music_player(object):
    """ Central class to manage all the controls """

    def __init__(self, volume, lastSongPath, view):
        self.vol = volume
        self.currSongPath = lastSongPath,
        self.view = view
        self.vol_cntrl = Volume_control( volume, self.set_volume)

    def start_loop(self):
        try:
            continu = True
            while continu:
                """ handle Events """

                sleep(0.001)

        finally:
            GPIO.cleanup()

        #handle Button Presses
        #continu = bi.check_buttons()
    """
    for i in range (0,11):
        v.draw_battery(100-i*10)
        sleep(1)"""
