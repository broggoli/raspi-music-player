import json

class Load_Settings(object):

    def __init__(self, settings_path = "../../raspi-music-player/settings/settings.json"):
        self.settings = json.load(open(settings_path))
        self.pins = self.get_pin_dict()
        self.lastSongPath = self.get_last_song_path()

    def get_settings(self):
        return self.settings, self.pins, self.lastSongPath

    def get_last_song_path(self):
        parts = (self.settings["music_dir"], self.settings["last_playlist"], self.settings["last_song"])
        return "/".join(parts)
    def get_pin_dict(self):
        pin_dict = {}
        for pin in self.settings["GPIO_Pins"]:
            pin_dict[pin["name"]] = pin["pinNr"]
        return pin_dict

    def print_pins(self):
        space = 30
        for pin in self.pins:
            print("Pin name: %s -->    Pin: %i" %((pin + " "*(space-len(pin))), self.pins[pin]))
        return True

ls = Load_Settings()
print(ls.last_song_path)
ls.print_pins()
