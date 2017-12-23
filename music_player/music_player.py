""" Music player app"""

from time import sleep

#importing the hrdware controls
from .controls.hardware_control.button_control import Button_Control
from .controls.hardware_control.rotary_encoder_control import Rotary_Encoder_Control

#importing the software controls
from .controls.software_control.song_control import Song_Control
from .controls.software_control.volume_control import Volume_Control
from .controls.software_control.display_control import Display_Control

class Music_player(object):
    """
        Central class to manage all the controls
        It ties together the hardware components with the software side.
    """

    def __init__(self):
        #Setting up all the GPIO pins

        #Individual button
        NEXT_SONG_BUTTON_PIN = 9
        #Individual button
        PREVIOUS_SONG_BUTTON_PIN = 25
        #This is the button of the rotary encoder
        PLAY_PAUSE_PIN = 7
        #Rotary_Encoder Buttons -> encode the rotation of the dial
        CLOCK_PIN = 27
        DATA_PIN = 18

        #loading the settings
        self.settings = json.load(open("../raspi-music-player/settings/settings.json"))

        #setting up the display
        self.display_control = Display_Control()
        #setting up the volume control dial -> is also the play&pause button
        self.volume_control = Volume_Control( self.settings["volume"])
        self.song_control = Song_Control(self.settings["lastSongPath"])


        #Setting up the hardware components and tieing them to the respective function
        self.volume_control_dial = Rotary_Encoder_Control(clockPin, dataPin,
                                            self.volume_control.change_volume)
        #setting up the song control buttons
        self.next_song_button = Button_Control(NEXT_SONG_BUTTON_PIN,
                                            self.song_control.next_song)
        self.previous_song_button = Button_Control(PREVIOUS_SONG_BUTTON_PIN,
                                            self.song_control.previous_song)
        self.play_pause_button = Button_Control(PLAY_PAUSE_PIN,
                                            self.song_control.play_pause)

    def start(self):
        #starting the event listeners
        print("Started!")
        self.volume_control_dial.start()
        self.play_pause_button.start()
        self.next_song_button.start()
        self.previous_song_button.start()
        self.view.start()
        self.start_loop()

    def stop(self):
        self.volume_control_dial.stop()
        self.play_pause_button.stop()
        self.next_song_button.stop()
        self.previous_song_button.stop()
        self.view.stop()
        print("Stopped!")

    def start_loop(self):
        try:
            continu = True
            while continu:
                #handle Events
                sleep(0.01)
                if(raw_input() != ""):
                    continu = False
                    print("Terminated the program!")
        finally:
            self.stop()
            GPIO.cleanup()

        #handle Button Presses
        #continu = bi.check_buttons()

    """for i in range (0,11):
        v.draw_battery(100-i*10)
        sleep(1)"""
