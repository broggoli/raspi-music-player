""" launcher program for the music player """
import music_player.music_player as mp

def main():
    try:
        music_player = mp.Music_player()
        music_player.start()
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
