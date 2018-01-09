#importing the hardware controls
from hardware_control.button_control import Button_Control
from hardware_control.rotary_encoder_control import Rotary_Encoder_Control

from software_control.song_control import Song_Control
from software_control.volume_control import Volume_Control

from datetime import datetime
from time import sleep

class Action_Control(object):

    def __init__(self, settings, view):
        self.settings = settings
        self.view = view

        self.settingsDir, self.pins = self.settings.load()

        self.currentlyPressed = {}
        self.longPushTime = 1

        #setting up the volume control dial -> is also the play&pause button
        self.volume_control = Volume_Control( self.settingsDir["volume"])
        self.song_control = Song_Control()

        #Setting up the hardware components and tieing them to the respective function
        self.volume_control_dial = Rotary_Encoder_Control(self.pins["CLOCK_PIN"], self.pins["DATA_PIN"],
                                                            self.volume_control.change_volume,
                                                            self.view.update_volume_view)
        #setting up the song control buttons
        self.next_song_button = Button_Control(self.pins["NEXT_SONG_BUTTON_PIN"],
                                            self.push_log,
                                            longClickCallback = True)
        self.previous_song_button = Button_Control(self.pins["PREVIOUS_SONG_BUTTON_PIN"],
                                            self.push_log,
                                            longClickCallback = True)
        self.shut_down_button = Button_Control(self.pins["SHUT_DOWN_BUTTON_PIN"],
                                            self.push_log)
        self.play_pause_button = Button_Control(self.pins["PLAY_PAUSE_BUTTON_PIN"],
                                            self.push_log,
                                            longClickCallback = True,
                                            pullDown = False)

    def start(self):
        self.volume_control_dial.start()
        self.play_pause_button.start()
        self.next_song_button.start()
        self.previous_song_button.start()
        self.shut_down_button.start()

    def stop(self):
        self.volume_control_dial.stop()
        self.play_pause_button.stop()
        self.next_song_button.stop()
        self.previous_song_button.stop()
        self.shut_down_button.stop()

    def push_log(self, pinNr, clicked):
        if pinNr in self.currentlyPressed:

            if self.currentlyPressed[pinNr]["start"] == 0 and clicked:
                self.currentlyPressed[pinNr] = {"clicked": clicked, "start": datetime.now()}

            timeElapsed = (datetime.now() - self.currentlyPressed[pinNr]["start"]).seconds
            if clicked:
                if timeElapsed >= self.longPushTime:
                    self.determin_push_action(pinNr, True)
                    sleep(0.3)
            else:
                if timeElapsed < self.longPushTime:
                    self.determin_push_action(pinNr)
                self.currentlyPressed[pinNr] = {"clicked": clicked, "start": 0}
        else:
            self.currentlyPressed[pinNr] = {"clicked": clicked, "start": datetime.now()}

        #print(pinNr, self.currentlyPressed[pinNr]["start"], clicked)

    def determin_push_action(self, pinNr, longPush=False):

        if longPush:
            if pinNr == self.next_song_button.bttn:
                self.song_control.fast_forward()
            elif pinNr == self.previous_song_button.bttn:
                self.song_control.rewind()
            elif pinNr == self.play_pause_button.bttn:
                #self.song_control.play_pause()
                print("one folder up!")
        else:
            if pinNr == self.next_song_button.bttn:
                self.song_control.next_song()
            if pinNr == self.previous_song_button.bttn:
                self.song_control.previous_song()
            if pinNr == self.play_pause_button.bttn:
                self.song_control.play_pause()

    def handleKeyInputs(self):
        inpt = raw_input()
        if inpt == "q":
            self.shut_down()
        elif inpt == "n":
            self.view.list_visual.select(nextSong = True)
        elif inpt == "b":
            self.view.list_visual.select(nextSong = False)
        elif inpt == "p":
            print(self.view.list_visual.down())
        elif inpt == "o":
            print(self.view.list_visual.up())
        elif inpt == "r":
            self.view.start()
        elif representsInt(inpt):
            self.volume_control.set_volume(int(inpt)*10,
            self.view.update_volume_view)
        self.view.update_view()
#Helper functions
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
