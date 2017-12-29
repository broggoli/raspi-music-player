""" Music player app"""

from time import sleep
from RPi import GPIO

#importing the hrdware controls
from .controls.hardware_control.button_control import Button_Control
from .controls.hardware_control.rotary_encoder_control import Rotary_Encoder_Control

#importing the software controls
from .controls.software_control.song_control import Song_Control
from .controls.software_control.volume_control import Volume_Control
from .controls.software_control.view import View
from load_settings import Load_Settings

class Music_player(object):
    """
        Central class to manage all the controls
        It ties together the hardware components with the software side.
    """

    def __init__(self):
        #Setting up all the GPIO pins

        #loading the settings
        self.settings, self.pins, self.lastSongPath = Load_Settings().get_settings()

        #setting up the display
        self.view = View()
        #setting up the volume control dial -> is also the play&pause button
        self.volume_control = Volume_Control( self.settings["volume"])
        self.view.volume_view.show(self.settings["volume"])
        self.song_control = Song_Control(self.lastSongPath)

        #Setting up the hardware components and tieing them to the respective function
        self.volume_control_dial = Rotary_Encoder_Control(self.pins["CLOCK_PIN"], self.pins["DATA_PIN"],
                                                            self.volume_control.change_volume,
                                                            self.view.volume_view.show)
        #setting up the song control buttons
        self.next_song_button = Button_Control(self.pins["NEXT_SONG_BUTTON_PIN"],
                                            self.song_control.next_song)
        self.previous_song_button = Button_Control(self.pins["PREVIOUS_SONG_BUTTON_PIN"],
                                            self.song_control.previous_song)
        self.play_pause_button = Button_Control(self.pins["PLAY_PAUSE_PIN"],
                                            self.song_control.play_pause,
                                            pullDown=False)
    def start(self):
        #starting the event listeners
        print("Started!")
        self.volume_control_dial.start()
        self.play_pause_button.start()
        self.next_song_button.start()
        self.previous_song_button.start()
        self.start_loop()

    def stop(self):
        self.volume_control_dial.stop()
        self.play_pause_button.stop()
        self.next_song_button.stop()
        self.previous_song_button.stop()
        print("Stopped!")

    def start_loop(self):
        try:
            continu = True
            while continu:
                inpt = raw_input()
                #handle Events
                sleep(0.5)
                if inpt == "q":
                    continu = False
                    print("Terminated the program!")
                elif inpt == "n":
                    self.song_control.next_song()
                elif inpt == "m":
                    self.song_control.previous_song()
                elif inpt == "p":
                    self.song_control.play_pause()
                elif representsInt(inpt):
                    self.volume_control.set_volume(int(inpt)*10,
                    self.view.volume_view.show)

        finally:
            self.stop()
            GPIO.cleanup()

"""for i in range (0,11):
    v.draw_battery(100-i*10)
    sleep(1)"""
#Helper functions
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
