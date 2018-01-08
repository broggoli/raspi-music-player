import json

class Settings(object):

    def __init__(self, settingsPath = "../raspi-music-player/settings/settings.json"):
        self.settingsPath = settingsPath
        self.settings = json.load(open(self.settingsPath))
        self.pins = self.get_pin_dict()

    def load(self):
        return self.settings, self.pins

    def save(self, volume=None, currentSong=None, currentDir=None):
        if volume and currentSong and currentDir:
            if volume:
                self.settings["volume"] = volume
            if currentSong:
                self.settings["lastSong"] = currentSong
            if currentDir:
                self.settings["lastDir"] = currentDir

            with open(self.settingsPath, 'w') as f:
                json.dump(self.newSettings, f)
                
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
