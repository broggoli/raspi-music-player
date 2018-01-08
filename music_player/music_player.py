""" Music player app"""

from time import sleep
from RPi import GPIO

from controls.action_control import Action_Control
#importing the software controls
from settings import Settings
import list_manager as lm
from controls.software_control.view import View

class Music_player(object):
    """
        Central class to manage all the controls
        It ties together the hardware components with the software side.
    """

    def __init__(self):
        self.shutDown = False

        #loading the settings from the json file
        self.settings = Settings()
        self.settings.print_pins()
        self.settingsDict, self.pins = self.settings.load()

        self.dir_list = lm.Dir_List(self.settingsDict["musicDir"], self.settingsDict["lastDir"])
        self.playlist = lm.Playlist(self.dir_list)

        if self.settingsDict["songView"] == "True":
            listToDisplay, listName = self.playlist.songs, self.playlist.name
        else:
            listToDisplay, listName = self.dir_list.get_top_branches(), self.dir_list.name

        self.view = View(self.settingsDict, (listToDisplay, listName))
        self.action_control = Action_Control(self.settings, self.view)



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
        #self.settings.save(self.volume, "The Kooks - Naive", "playlist1")
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
