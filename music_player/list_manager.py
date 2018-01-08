import os
from random import random

class List_Manager(object):

    def __init__(self, musicDir):
        self.musicDir = musicDir
        self.songTree = self.get_song_tree(self.musicDir)

    def get_song_tree(self, directory, dirName=None):

        if dirName:
            tree = {0 : dirName}
        else:
            #The top directory is called "All your music" in swiss german
            tree = {0: "Alli dini Lieder"}

        dirList = os.listdir(directory)
        firstSong = True

        for i, d in enumerate(dirList):
            if os.path.isdir(directory+"/"+d):
                tree[d] = self.get_song_tree(directory+"/"+d, dirName=d)
            elif d.endswith(".mp3"):
                if firstSong:
                    tree["songs"] = [dirName]
                    firstSong = False
                tree["songs"].append(d)
        return tree

class Dir_List(List_Manager):

    def __init__(self, rootDir, directory):
        super(Dir_List, self).__init__(rootDir)
        self.rootDir = rootDir
        self.directory = directory

        self.set_name()

    def set_name(self):
        if self.directory == "":
            self.name = "Alli dini Lieder"
        else:
            self.name = self.directory

    def change_dir(self, directory):
        self.directory = directory
        self.set_name()

    def get_tree(self, tree=None, firstCall=True, found=False):
        """ recursively searches through the given directory and returns a tree
            of dictionaries with all the songs listed """
        if firstCall:
            tree = self.songTree
        if self.directory == "":
            return tree
        if not found:
            for branch in tree:
                if branch > 0:
                    if branch == self.directory:
                        return self.get_list(tree[branch], False, True)

                    if not "songs" in tree and len(tree) < 1:
                        return self.get_list(tree[branch], False, False)

        else:
            if tree == None:
                print("No such Directory!")
            return tree

    def get_top_branches(self):
        l = self.get_tree()
        topBranches = []
        for branch in l:
            topBranches.append(branch)
        return topBranches

class Playlist():

    def __init__(self, dir_list, shuffle = False):
        self.dirList = dir_list.get_tree()
        self.shuffle = shuffle

        if self.dirList != None:
            self.name = self.dirList[0]
        else:
            self.name = "Unknown"

        self.list, self.paths = self.makePlaylist(self.dirList, dir_list.directory)
        self.songs = self.raw_to_song_display_name(self.order(self.list))

    def order(self, l):
        if self.shuffle:
            shuffled = sorted(l, key=lambda k: random())
            return shuffled
        else:
            return sorted(l)
    def makePlaylist(self, l, path = ""):
        """ returns a list of all the songs and a list with all the paths in the directory (also sub dirs) """
        if l:
            songList, pathList = [], []
            for c, item in enumerate(l):
                if c > 0:
                    if item == "songs":
                        i = [x for e,x in enumerate(l[item]) if e > 0]
                        songList.extend(i)
                        pathList.append(path+"/"+l[0])
                    else:
                        s, p = self.makePlaylist(l[item], path+"/"+l[0])
                        #song_name = self.raw_to_song_display_name(s)
                        songList.extend(s)
                        pathList.extend(p)
            return songList, pathList
        else:
            return None

    def raw_to_song_display_name(self, rawNames):
        """ returns the song name without the '.mp3' and the song number, if there is one"""
        cleanNames = []
        for rawName in rawNames:
            nameParts = rawName.split(".")
            print(rawName)
            for part in nameParts:
                if part != "mp3" and not representsInt(part):
                    cleanNames.append(part.strip(" "))
        return cleanNames

class List_Visual(object):

    def __init__(self, settingsDict):
        self.settingsDict = settingsDict
        self.dir_list = Dir_List(self.settingsDict["musicDir"], self.settingsDict["lastDir"])
        self.playlist = lm.Playlist(self.dir_list)

        if self.settingsDict["songView"] == "True":
            self.currentList, self.currentListName  = self.playlist.songs, self.playlist.name
        else:
            self.currentList, self.currentListName = self.dir_list.get_top_branches(), self.dir_list.name

        #setting the currently Selected song
        self.currentlySelected = self.settings["lastSongIndex"]
        self.itemsPerPage = 6
        self.currentPage = 1

        self.amount_pages()
        self.visible_list(self.currentlySelected)

    def amount_pages(self):
        self.totalPages = max(1, int(math.ceil(len(self.currentList) / self.itemsPerPage)))

    def select(self, nextSong=None, index=None):

        print("currentlySelected", self.currentlySelected)
        if index:
            #select the given index
            self.visibleList = self.visible_list(index)
        else:
            if nextSong == True:
                #select next song and return the list
                self.visibleList = self.visible_list(self.currentlySelected + 1)
            elif nextSong == False:
                #select previous song list
                self.visibleList = self.visible_list(self.currentlySelected - 1)

    def visible_list(self, proposedSelected):
        firstItemIndex = self.itemsPerPage * ( self.currentPage - 1 )
        lastItemIndex = self.itemsPerPage * self.currentPage - 1

        proposedSelected = min(len(self.currentList)-1, proposedSelected)
        proposedSelected = max(0, proposedSelected)

        self.currentPage = math.floor(proposedSelected/self.itemsPerPage) + 1
        self.currentlySelected = proposedSelected

        print("currentlySelected", self.currentlySelected)
        self.visibleList = [item for index, item in enumerate(self.currentList[1:])
                if index >= firstItemIndex and
                index <= lastItemIndex]

    def change_list(self, l=None, down=None):
        if l:
            self.currentList = l
        elif down:
            if down == True:
                #make the currently selected item the new directory
                directory = self.currentList[self.currentlySelected]
                self.dir_list.change_dir(directory)
                self.currentList, self.currentListName = self.dir_list.get_top_branches(), self.dir_list.name
            else:


        self.currentlySelected = 0
        self.amount_pages()

    def get_scroll_info(self):
        return (self.currentPage, self.totalPages)

#Helper functions
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
