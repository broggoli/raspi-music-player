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
        self.settingsDict = self.settings.load()

        self.state = State(self.settingsDict)

        self.list_visual = lm.List_Visual(self.state)

        self.view = View(self.state, self.list_visual)
        self.action_control = Action_Control(self.state, self.list_visual)

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
                    self.shutdown()
                    print("Terminated the program!")
                sleep(0.2)
        finally:
            self.stop()
            GPIO.cleanup()

    def shutdown(channel):
        cmd = "sudo wall 'System shutting down in %d seconds'" % self.shutdown_wait
        os.system(cmd)

        time.sleep(self.shutdown_wait)

        msg = time.strftime("User Request - Shutting down at %a, %d %b %Y %H:%M:%S +0000\n", time.gmtime())

        # open log file in append mode
        self.logfile_pointer = open(self.logfile, 'a+')
        self.logfile_pointer.write(msg)
        self.logfile_pointer.close()

        GPIO.cleanup()
        os.system("sudo shutdown now")
