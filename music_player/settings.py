import json

class Settings(object):

    def __init__(self, settingsPath):
        self.settingsPath = settingsPath
        self.settings = json.load(open(self.settingsPath), encoding="utf-8")

    def load(self):
        return self.settings

    def save(self, state):

        newSettings = {
                        "musicDir": self.settings["musicDir"],
                        "lastDirPath": state.currentDirPath,
                        "lastView": state.currentView,
                        "lastpageNr": state.currentPageNr,
                        "totalPages": state.currentTotalPages,
                        "lastSelected": state.currentlySelected,
                        "volume": state.currentVolume,
                        "itemsPerPage": self.settings["itemsPerPage"],
                        "GPIOpins": self.settings["GPIOpins"]
                    }

        with open(self.settingsPath, 'w') as f:
            json.dump(newSettings, f, ensure_ascii=False)

    def print_pins(self):
        """ prints all the GPIOpins that are used by the musicplayer app """
        print("-"*8 + " GPIO mode: BMC " +"-"*8)

        space = 30
        for pin in self.settings["GPIOpins"]:
            print("Pin name: %s -->    Pin: %i" %((pin + " "*(space-len(pin))), self.settings["GPIOpins"][pin]))
        return True
