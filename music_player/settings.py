import json

class Load_Settings(object):

    def __init__(self, settingsPath = "../raspi-music-player/settings/settings.json"):
        self.settings = json.load(open(settingsPath))
        self.pins = self.get_pin_dict()

    def get_settings(self):
        return self.settings, self.pins

    def get_last_song_path(self):
        parts = (self.get_last_playlist(), self.settings["lastSong"])
        return "/".join(parts)

    def get_last_playlist(self):
        parts = (self.settings["musicDir"], self.settings["lastPlaylist"])
        return "/".join(parts)

    def get_pin_dict(self):
        pin_dict = {}
        for pin in self.settings["GPIOpins"]:
            pin_dict[pin["name"]] = pin["pinNr"]
        return pin_dict

    def print_pins(self):
        space = 30
        for pin in self.pins:
            print("Pin name: %s -->    Pin: %i" %((pin + " "*(space-len(pin))), self.pins[pin]))
        return True

class Save_Settings(object):

    def __init__(self, settingsPath = "../raspi-music-player/settings/settings.json"):
        self.settingsPath = settingsPath
        self.newSettings = json.load( open(settingsPath) )

    def save(self, volume, currentSong, currentPlayist):
        self.newSettings["volume"] = volume
        self.newSettings["lastSong"] = currentSong
        self.newSettings["lastPlaylist"] = currentPlayist

        with open(self.settingsPath, 'w') as f:
            json.dump(self.newSettings, f)
