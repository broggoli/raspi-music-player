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
        
        if directory == "":
            self.name = "Alli dini Lieder"
        else:
            self.name = self.directory

    def get_list(self, tree=None, firstCall=True, found=False):
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

                    if not "songs" in tree and len(tree) <= 2:
                        return self.get_list(tree[branch], False, False)

        else:
            if tree == None:
                print("No such Directory!")
            return tree

    def get_top_branches(self):
        l = self.get_list()
        topBranches = []
        for branch in l:
            if not representsInt(branch):
                topBranches.append(branch)
        return topBranches

class Playlist():

    def __init__(self, dir_list, shuffle = False):
        self.dirList = dir_list.get_list()
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
        """ returns a list of all the songs and a list wit hall the paths in the directory (also sub dirs) """
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

#Helper functions
def representsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
