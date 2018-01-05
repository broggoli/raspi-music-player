""" Music player app"""

from time import sleep
from RPi import GPIO

from controls.action_control import Action_Control
#importing the software controls
from settings import Load_Settings
from settings import Save_Settings
from playlist_manager import Playlist
from controls.software_control.view import View

class Music_player(object):
    """
        Central class to manage all the controls
        It ties together the hardware components with the software side.
    """

    def __init__(self):
        self.shutDown = False

        #loading the settings
        self.lSettings = Load_Settings()
        self.sSettings = Save_Settings()
        self.lSettings.print_pins()
        self.settings, self.pins = self.lSettings.get_settings()

        self.playlist = Playlist(self.settings["musicDir"], self.settings["lastPlaylist"])

        self.view = View(self.settings, self.playlist)

        self.action_control = Action_Control(self.lSettings, self.view)

        print(self.playlist.list)


    def start(self):
        #starting the event listeners
        print("Started!")
        self.action_control.start()
        self.view.start()
        self.start_loop()

    def shut_down(self):
        self.shutDown = True

    def stop(self):
        self.action_control.stop()
        #self.sSettings.save(60, "The Kooks - Naive", "playlist1")
        print("Stopped!")

    def start_loop(self):
        try:
            continu = True
            while continu:
                #handle Events
                """Activate when no buttons are available"""
                self.action_control.handleKeyInputs();
                if self.shutDown:
                    continu = False
                    print("Terminated the program!")
                sleep(0.5)
        finally:
            self.stop()
            GPIO.cleanup()
