from datetime import datetime

class State(object):

    def __init__(self, settings):
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
        self.pinStates = { pin: 0 for pin in settings["GPIOpins"] } #self.initializePinStates(self.settings["GPIOpins"])
        self.displayed = False

        #define
        self.play = "False"

    def update(self):
        self.displayed = False
        self.lastUpdated = datetime.now()
        #print("updated")

    def initializePinStates(self, pins):
        ps = {}
        for pin in pins:
            pinNr = pins[pin]
            ps[pinNr] = {"actionStart": 0}

        return ps

    def list_name(self):
        return "Alli dini Lieder" if self.currentDir == "" else self.currentDir
