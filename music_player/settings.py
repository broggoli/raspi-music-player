import json

class Settings(object):

    def __init__(self, settingsPath = "../raspi-music-player/settings/settings.json"):
        self.settingsPath = settingsPath
        self.settings = json.load(open(self.settingsPath), encoding="utf-8")

    def load(self):
        return self.settings

    def save(self, volume=None, currentSong=None, currentDir=None):
        if volume and currentSong and currentDir:
            if volume:
                self.settings["volume"] = volume
            if currentSong:
                self.settings["lastSong"] = currentSong
            if currentDir:
                self.settings["lastDir"] = currentDir

            with open(self.settingsPath, 'w') as f:
                json.dump(self.newSettings, f, ensure_ascii=False)

    def print_pins(self):
        """ prints all the GPIOpins that are used by the musicplayer app """
        print("-"*8 + " GPIO mode: BMC " +"-"*8)

        space = 30
        for pin in self.settings["GPIOpins"]:
            print("Pin name: %s -->    Pin: %i" %((pin + " "*(space-len(pin))), self.settings["GPIOpins"][pin]))
        return True
