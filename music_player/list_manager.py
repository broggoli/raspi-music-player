import os
from random import random
import math

class List_Manager(object):

    def __init__(self, musicDir):
        self.musicDir = musicDir
        self.directoryTree = self.get_tree(self.musicDir)

    def get_tree(self, directory, dirName=None):

        if dirName:
            tree = {0 : dirName}
        else:
            tree = {0: self.musicDir}

        dirList = os.listdir(directory)
        firstSong = True

        for i, d in enumerate(dirList):
            if os.path.isdir(directory+"/"+d):
                tree[d] = self.get_tree(directory+"/"+d, dirName=d)
            elif d.endswith(".mp3"):
                if firstSong:
                    tree["songs"] = [dirName]
                    firstSong = False
                tree["songs"].append(d)
        return tree

    def getTreeFromPath(self, path, t=None, c=1):
        if t == None:
            t = self.directoryTree
        if c < len(path):
            return self.getTreeFromPath(path, t[path[c]], c+1)
        else:
            return t

class Dir_List(List_Manager):

    def __init__(self, rootDir, directory):
        super(Dir_List, self).__init__(rootDir)
        self.rootDir = rootDir
        self.set_dir(directory)

    def set_name(self):
        self.name = "Alli dini Lieder" if self.directory == "" else self.directory

    def set_dir(self, directory=None, path=None):
        if directory != None:
            self.directory = directory
            self.pathToCurrentDir = self.get_path(pathSoFar=[])
        else:
            self.directory = path[-1]
            self.pathToCurrentDir = path
        #A bit inefficient, which hurts my programmer heart, but don't have time to find a more elegant solution
        #just searches the whole Tree
        self.dirTree = self.getTreeFromPath(self.pathToCurrentDir)
        self.set_name()

    def moveOneUp(self):
        print(self.pathToCurrentDir)
        if len(self.pathToCurrentDir) > 2:
            p = self.pathToCurrentDir[:-1]
            self.set_dir(path=p)
        else:
            self.set_dir("")

    def moveOneDown(self, directory):
        if directory in self.dirTree:
            path = list(self.pathToCurrentDir)
            path.append(directory)
            self.directory = path[-1]
            self.pathToCurrentDir = path
            self.dirTree = self.dirTree[self.directory]
            self.set_name()

    def get_path(self, tree=None, pathSoFar=[], found=False):
        """ recursively searches through the given directory and returns a tree
            of dictionaries with all the songs listed """
        if len(pathSoFar) == 0:
            tree = self.directoryTree
        if self.directory == "":
            return [self.rootDir]

        if not found:
            if self.directory in self.get_top_branches(tree):
                pathSoFar.append(tree[0])
                return pathSoFar
            for branch in tree:

                if not representsInt(branch):
                    if branch == self.directory:
                        pathSoFar.append(tree[0])
                        return self.get_path(tree[branch], pathSoFar, True)

                    if not "songs" in tree[branch]:
                        pathSoFar.append(tree[0])
                        return self.get_path(tree[branch], pathSoFar, False)

        else:
            pathSoFar.append(tree[0])
            return pathSoFar

        print("nothing found")
        return [self.rootDir]

    def get_top_branches(self, tree=None):
        topBranches = []
        if tree == None:
            tree = self.dirTree
        for branch in tree:
            topBranches.append(branch)
        return topBranches

    def order(self, l):
        if self.shuffle:
            shuffled = sorted(l, key=lambda k: random())
            return shuffled
        else:
            return sorted(l)

    def get_songs(self, shuffle = False):
        self.songPaths = self.get_mp3s(self.dirTree)
        self.songNames = self.extract_song_names(self.songPaths)
        return self.songNames

    def extract_song_names(self, songPaths):
        """ returns the song name without the '.mp3' and the song number, if there is one"""
        cleanNames = []
        for songPath in songPaths:
            rawName = songPath.split("/")[-1]
            nameParts = rawName.split(".")
            for part in nameParts:
                if part != "mp3" and not representsInt(part):
                    cleanNames.append(part.strip(" "))
        return cleanNames

    def get_mp3s(self, t, path = ""):
        """ returns a list of all the songs and a list with all the paths in the directory (also sub dirs) """
        if t:
            songPaths = []
            for c, item in enumerate(t):
                if c > 0:
                    if item == "songs":
                        songs = t[item][1:]
                        pathOfThisDir = path+"/"+t[0]
                        sp = [pathOfThisDir+"/"+s for s in songs]
                        return sp
                    else:
                        songPaths.extend(self.get_mp3s(t[item], path+"/"+t[0]))
            return songPaths
        else:
            return None

class List_Visual(object):

    def __init__(self, settingsDict):
        self.settingsDict = settingsDict
        self.itemsPerPage = 6
        self.dir_list = Dir_List(self.settingsDict["musicDir"], self.settingsDict["lastDir"])
        self.setupNewList(self.settingsDict["lastSongIndex"])
        self.currentView = self.settingsDict["currentView"]

    def currentList(self):
        l = self.dir_list.get_top_branches()
        if "songs" in l and len(l) <= 2:
            self.currentView = "playlist"
            return self.dir_list.get_songs()

        self.currentView = "directory"
        return self.dir_list.get_top_branches()[1:]

    def amount_pages(self):
        self.totalPages = int(math.ceil(len(self.currentList()) / self.itemsPerPage)) + 1

    def select(self, nextSong=None, index=None):

        if index:
            #select the given index
            self.visibleList = self.visible_list(index)
        else:
            if nextSong == True:
                #select next song and return the list
                self.visible_list(self.currentlySelected + 1)
            elif nextSong == False:
                #select previous song list
                self.visible_list(self.currentlySelected - 1)

    def trimForDisplay(self, string):
        maxLen=13
        if len(string) <= maxLen:
            return string
        else:
            return string[:maxLen] + "..."

    def visible_list(self, proposedSelected):

        cl = self.currentList()
        # Limit the maximal selectable index to the last index of the list
        proposedSelected = min(len(cl)-1, proposedSelected)
        proposedSelected = max(0, proposedSelected)

        self.currentPage = int(math.floor(proposedSelected/self.itemsPerPage) + 1)
        self.currentlySelected = proposedSelected

        firstItemIndex = self.itemsPerPage * ( self.currentPage - 1 )
        lastItemIndex =  self.itemsPerPage * self.currentPage - 1
        self.highlited = self.currentlySelected % self.itemsPerPage

        if len(cl) > 0:
            self.visibleList = [item for index, item in enumerate(cl)
                    if index >= firstItemIndex and
                    index <= lastItemIndex]
        else:
            self.visibleList = ["Da hets nix drin..."]

        self.visibleList = map(self.trimForDisplay, self.visibleList)
    def change_list(self, directory=None):
        self.dir_list.set_dir(directory)

    def down(self):
        cl = self.currentList()
        if len(cl) > 0:
            if self.currentView == "directory":
                #make the currently selected item the new directory
                directory = cl[self.currentlySelected]
                self.dir_list.moveOneDown(directory)
                self.setupNewList(0)
                return "moved Down"
            else:
                return "Play"
    def up(self):
        if self.currentView == "playlist":
            self.currentView == "directory"

        """ For later, to have the same folder selected that has just been exited"""
        dirIndex = 0
        self.dir_list.moveOneUp()
        self.setupNewList(dirIndex)
        return "Pause"

    def setupNewList(self, selected):
        self.listName = self.dir_list.name
        self.currentPage = 1
        self.currentlySelected = selected
        self.amount_pages()
        self.visible_list(self.currentlySelected)

    def get_scroll_info(self):
        return (self.currentPage, self.totalPages)

#Helper functions
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
