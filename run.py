""" launcher program for the music player """
import music_player.music_player as mp
from music_player.controls.view import View
import json

def main():
    #load log
    log = json.load(open('settings/settings.json'))

    #calculate battery percentage -> for now just simulating
    batteryPercentage = 60

    #initialize the Display
    v = View( batteryPercentage )
    """bi = Button_interface(v)"""

    #showLoadingScreen()
    #lad log

    music_player = mp.Music_player(log["volume"], log["lastSongPath"], v)
    #music_player.start_loop()

if __name__ == "__main__":
    main()
