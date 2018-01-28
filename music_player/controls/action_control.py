#importing the hardware controls
from hardware_control.button_control import Button_Control
from hardware_control.rotary_encoder_control import Rotary_Encoder_Control
from hardware_control.battery_control import Battery_Control

from software_control.song_control import Song_Control
from software_control.volume_control import Volume_Control

from datetime import datetime
from datetime import timedelta
from time import sleep

class Action_Control(object):

    def __init__(self, settings, state, list_visual):
        self.settings = settings
        self.state = state
        self.list_visual = list_visual
        self.running = True

        self.longPushTime = 1

        #setting up the volume control dial -> is also the play&pause button
        self.volume_control = Volume_Control(self.state)
        self.song_control = Song_Control(self.state)
        self.battery_control = Battery_Control(self.settings["GPIOpins"], self.state, shutdown_callback = self.terminate_loop)

        #Setting up the hardware components and tieing them to the respective function
        self.volume_control_dial = Rotary_Encoder_Control(self.settings["GPIOpins"]["CLOCK_PIN"], self.settings["GPIOpins"]["DATA_PIN"],
                                                            self.rotary_log)
        #setting up the song control buttons
        self.next_song_button = Button_Control(self.settings["GPIOpins"]["NEXT_SONG_BUTTON_PIN"],
                                            self.push_log,
                                            longClickCallback = True)
        self.previous_song_button = Button_Control(self.settings["GPIOpins"]["PREVIOUS_SONG_BUTTON_PIN"],
                                            self.push_log,
                                            longClickCallback = True)
        self.play_pause_button = Button_Control(self.settings["GPIOpins"]["PLAY_PAUSE_BUTTON_PIN"],
                                            self.push_log,
                                            longClickCallback = True,
                                            pullDown = False)

    def start(self):
        self.volume_control_dial.start()
        self.play_pause_button.start()
        self.next_song_button.start()
        self.previous_song_button.start()
        self.battery_control.start()

    def stop(self):
        self.volume_control_dial.stop()
        self.play_pause_button.stop()
        self.next_song_button.stop()
        self.previous_song_button.stop()
        self.battery_control.stop()

    def rotary_log(self, clockwise):
        self.volume_control.change_volume(clockwise)
        self.state.update()

    def push_log(self, pinNr, clicked):

        if pinNr in self.state.buttonPinStates:

            if self.state.buttonPinStates[pinNr] ==  timedelta(0) and clicked:
                self.state.buttonPinStates[pinNr] = datetime.now()

            if not clicked:
                self.state.buttonPinStates[pinNr] = timedelta(0)
        else:
            print("pin not initialized!")

        self.determin_push_action()

        """print("next "+str(self.timeElapsed(self.state.buttonPinStates[26])),
            "| previous "+str(self.timeElapsed(self.state.buttonPinStates[20])),
            "| playpause: "+ str(self.timeElapsed(self.state.buttonPinStates[16])))
"""
    def timeElapsed(self, startingTime):
        if startingTime == timedelta(0):
            return -1
        else:
            return (datetime.now() - startingTime).seconds

    def determin_push_action(self, pinNr=None, longPush=False):
        """
            This is the callback function for all the buttons. It is necessary
            to have this to detect when two buttons are pressed simultanously

        """
        currentlyPressed = []
        for pinNr in self.state.buttonPinStates:
            #print("%i: %i" %(pinNr, self.timeElapsed(v)))

            if self.timeElapsed(self.state.buttonPinStates[pinNr]) != -1:
                currentlyPressed.append(pinNr)

        """if len(currentlyPressed) > 1:
            #giving all the simultanously pushed buttons the same starting time
            pushTime = self.timeElapsed(self.state.buttonPinStates[currentlyPressed[0]])
            for i in range(len(currentlyPressed)):
                self.state.buttonPinStates[currentlyPressed[i]] = pushTime

                print("two buttons pressed!")"""
        if len(currentlyPressed) == 1:
            pinNr = currentlyPressed[0]
            pushTime = self.timeElapsed(self.state.buttonPinStates[pinNr])
            if pushTime > 1:
                if pinNr == self.next_song_button.bttn:
                    self.song_control.fast_forward()
                elif pinNr == self.previous_song_button.bttn:
                    self.song_control.rewind()
                elif pinNr == self.play_pause_button.bttn:
                    #self.song_control.play_pause()
                    print(self.list_visual.up())
            else:
                if pinNr == self.next_song_button.bttn:
                    #self.song_control.next_song()
                    self.list_visual.select(nextEntry = True)
                if pinNr == self.previous_song_button.bttn:
                    #self.song_control.previous_song()
                    self.list_visual.select(nextEntry = False)
                if pinNr == self.play_pause_button.bttn:
                    self.song_control.play_pause()
                    print(self.list_visual.down())

        self.state.update()

    """def handleKeyInputs(self):
        inpt = raw_input()
        if inpt == "q":
            self.terminate_loop()
        elif inpt == "n":
            self.view.list_visual.select(nextEntry = True)
        elif inpt == "b":
            self.view.list_visual.select(nextEntry = False)
        elif inpt == "p":
            print(self.view.list_visual.down())
        elif inpt == "o":
            print(self.view.list_visual.up())
        elif inpt == "r":
            self.view.start()
        elif representsInt(inpt):
            self.volume_control.set_volume(int(inpt)*10,
            self.view.update_volume_view)
        self.view.update_view()"""

    def terminate_loop(self):
        print("Terminating loop")
        self.running = False

#Helper functions
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
