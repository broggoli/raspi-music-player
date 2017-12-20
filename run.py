""" launcher program for the music player """
import music_player as mp
from controls.view import View

def main():
    volume = 60
    batteryPrercentage = 50
    lastSongPath = "path/to/last/song"

    #initialize the Display
    v = View( batteryPrercentage )
    """bi = Button_interface(v)"""

    #showLoadingScreen()
    #lad log

    music_player = mp.Music_player(volume, lastSongPath, v)
    music_player.start_loop()


if __name__ == "__main__":
    main()
