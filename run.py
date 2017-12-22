""" launcher program for the music player """
import music_player.music_player as mp
import json

def main():
    #load log
    log = json.load(open('settings/settings.json'))

    #showLoadingScreen()
    #lad log

    music_player = mp.Music_player(log["volume"], log["lastSongPath"])
    music_player.start()
    #music_player.start_loop()

if __name__ == "__main__":
    main()
