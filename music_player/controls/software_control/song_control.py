import os
class Song_Control(object):

    def __init__(self, state):
        #initially the song is paused
        self.state = state
        #How many seconds does it rewind or fast forward
        self.jumpPercentage = 5

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
        os.system("mpc seek +%i" %self.jumpPercentage)
        print("Fast forward!")
    def rewind(self):
        os.system("mpc seek -%i" %self.jumpPercentage)
        print("Rewind!")
