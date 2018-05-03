from datetime import datetime
from datetime import timedelta

class State(object):

    def __init__(self, settings):

        self.next_button = settings["GPIOpins"]["NEXT_SONG_BUTTON_PIN"]
        self.previous_button = settings["GPIOpins"]["PREVIOUS_SONG_BUTTON_PIN"]
        self.play_pause_button = settings["GPIOpins"]["PLAY_PAUSE_BUTTON_PIN"]

        #Insert from settings
        self.itemsPerPage = settings["itemsPerPage"]
        self.musicDir = settings["musicDir"]
        self.currentVolume = settings["volume"]
        self.currentView = settings["lastView"]
        self.currentDirPath = settings["lastDirPath"]
        self.currentPageNr = settings["lastpageNr"]
        self.currentTotalPages = settings["totalPages"]
        self.currentlyVisibleList = settings["lastView"]
        self.currentlySelected = settings["lastSelected"]
        self.currentlyHighlighted = self.currentlySelected % self.itemsPerPage

        #calculate
        self.lastUpdated = datetime.now()
        self.currentDir = self.currentDirPath[-1]
        self.currentListName = self.list_name()
        self.buttonPinStates = {
                                    self.next_button        : timedelta(0),
                                    self.previous_button    : timedelta(0),
                                    self.play_pause_button  : timedelta(0),
                                }
        self.lowBattery = False
        self.displayed = False

        #define
        self.play = False

    def update(self):
        self.displayed = False
        self.lastUpdated = datetime.now()
        #print("updated")

    def list_name(self):
        return "Alli dini Lieder" if self.currentDir == "" else self.currentDir
