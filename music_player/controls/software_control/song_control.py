import os
class Song_Control(object):

    def __init__(self, state):
        #initially the song is paused
        self.state = state

    def play_pause(self):
        if self.state.play:
            print("Play!")
            self.state.play = True
        else:
            print("Pause!")
            self.state.play = False

        os.system("mpc toggle")

    def next_song(self):
        """ for now just mockup"""
        os.system("mpc next")
        print("playing next song!")

    def previous_song(self):
        """ for now just mockup"""
        os.system("mpc prev")
        print("playing previous song!")

    def get_play_state(self):
        return self.isPaused

    def fast_forward(self):
        """ for now just mockup"""
        print("Fast forward!")
    def rewind(self):
        """ for now just mockup"""
        print("Rewind!")
