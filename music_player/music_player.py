""" Music player app"""

from time import sleep
from RPi import GPIO

from controls.action_control import Action_Control
#importing the software controls
from settings import Settings
import list_manager as lm
from controls.software_control.view import View
from state import State

class Music_player(object):
    """
        Central class to manage all the controls
        It ties together the hardware components with the software side.
    """

    def __init__(self):
        #loading the settings from the json file
        self.settings = Settings()
        self.settings.print_pins()
        self.settingsDict, self.pins = self.settings.load()

        self.state = State(self.settingsDict)

        self.list_visual = lm.List_Visual(self.state)

        self.view = View(self.state, self.list_visual)
        self.action_control = Action_Control(self.pins, self.state, self.list_visual)

    def start(self):
        #starting the event listeners
        print("Started!")
        self.action_control.start()
        self.view.start()
        self.start_loop()

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
                #self.action_control.handleKeyInputs();
                self.view.update(self.state)
                if self.action_control.shutDown:
                    continu = False
                    print("Terminated the program!")
                sleep(0.05)
        finally:
            self.stop()
            GPIO.cleanup()
