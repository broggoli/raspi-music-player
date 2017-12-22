
class Song_Control(object):

    def __init__(self, lastSongPath):
        #initially the song is paused
        self.isPaused = True
        self.currentSong = lastSongPath

    def play_pause(self):
        if self.isPaused:
            print("Play!")
            self.isPaused = False
        else:
            print("Pause!")
            self.isPaused = True

    def next_song(self):
        """ for now just mockup"""
        print("playing next song!")

    def previous_song(self):
        """ for now just mockup"""
        print("playing previous song!")

    def get_play_state(self):
        return self.isPaused
