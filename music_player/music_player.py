""" Music player app"""

from time import sleep
from RPi import GPIO

from controls.view import View
from controls.volume_control import Volume_Control
from controls.button_control import Button_Control
from controls.song_control import Song_Control

class Music_player(object):
    """ Central class to manage all the controls """

    def __init__(self, volume, lastSongPath):
        #Setting up all the GPIO pins

        #Individual button
        NEXT_SONG_BUTTON_PIN =9;
        #Individual button
        PREVIOUS_SONG_BUTTON_PIN = 25;
        #This is the button of the rotary encoder
        PLAY_PAUSE_PIN = 7
        #Rotary_Encoder Buttons -> encode the rotation of the dial
        CLOCK_PIN = 27
        DATA_PIN = 18


        self.vol = volume

        #setting up the display
        self.view = View()
        #setting up the volume control dial -> is also the play&pause button
        self.volume_control = Volume_Control( volume, CLOCK_PIN, DATA_PIN)
        self.song_control = Song_Control(lastSongPath)

        #setting up the next/previous song buttons
        self.next_song_button = Button_Control(NEXT_SONG_BUTTON_PIN, self.song_control.next_song)
        self.previous_song_button = Button_Control(PREVIOUS_SONG_BUTTON_PIN, self.song_control.previous_song)
        self.play_pause_button = Button_Control(PLAY_PAUSE_PIN, self.song_control.play_pause)

    def start(self):
        #starting the event listeners
        print("Started!")
        self.volume_control.start()
        #self.play_pause_button.start()
        #self.next_song_button.start()
        #self.previous_song_button.start()
        self.view.start()


    """def start_loop(self):
        try:
            continu = True
            while continu:
                #handle Events

                sleep(0.001)

        finally:
            GPIO.cleanup()

        #handle Button Presses
        #continu = bi.check_buttons()

    for i in range (0,11):
        v.draw_battery(100-i*10)
        sleep(1)"""
