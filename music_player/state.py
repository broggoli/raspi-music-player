from datetime import datetime

class State(object):

    def __init__(self, settings):
        self.create_main_state_vars(settings)

    def create_main_state_vars(self, settings):
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
        self.displayed = False

        #define
        self.play = "False"

    def update(self):
        self.displayed = False
        self.lastUpdated = datetime.now()
        print(self.__dict__)
        print("updated")

    def list_name(self):
        return "Alli dini Lieder" if self.currentDir == "" else self.currentDir
