""" Music player app"""

import time
from RPi import GPIO
import os

import list_manager as lm
from controls.action_control import Action_Control
#importing the software controls
from settings import Settings
from controls.software_control.view import View
from state import State

class Music_player(object):
    """
        Central class to manage all the controls
        It ties together the hardware components with the software side.
    """

    def __init__(self):
        #loading the settings from the json file
        self.logfile = '/home/pi/raspi-music-player/battery_control.log'
        self.settingsPath = '/home/pi/raspi-music-player/settings/settings.json'

        self.settings = Settings(self.settingsPath)
        self.settings.print_pins()
        self.settingsDict = self.settings.load()

        self.state = State(self.settingsDict)

        self.list_visual = lm.List_Visual(self.state)

        self.view = View(self.state, self.list_visual)
        self.action_control = Action_Control(self.settingsDict, self.state, self.list_visual)

    def start(self):
        #starting the event listeners
        print("Started!")
        self.action_control.start()
        self.view.start()
        self.start_loop()

    def start_loop(self):
            continu = True
            while continu:
                #handle Events
                """Activate when no buttons are available"""
                #self.action_control.handleKeyInputs()
                self.view.update(self.state)

                continu = self.action_control.running

                if not continu:
                    print("Terminating the program and shutting down!")
                    self.action_control.stop()
                    self.settings.save(self.state)
                    self.shutdown()

            time.sleep(0.1)

    def shutdown(self):

        print("shutting down now!")

        os.system("sudo wall 'System shutting down'")

        if self.state.lowBattery:
            self.view.low_battery_display()
            lowBatteryText = " -> lowBattery"
        else:
            lowBatteryText = ""
            self.view.shut_down_display()

        msg = time.strftime("User Request - Shutting down at %a, %d %b %Y %H:%M:%S +0000\n", time.gmtime())
        msg += lowBatteryText

        # open log file in append mode
        self.logfile_pointer = open(self.logfile, 'a+')
        self.logfile_pointer.write(msg)
        self.logfile_pointer.close()

        GPIO.cleanup()
        os.system("sudo shutdown -h now")
