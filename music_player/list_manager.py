import os
from random import shuffle

class List_Manager(object):

    def __init__(self, musicDir):
        self.musicDir = musicDir
        self.songTree = self.get_song_tree(self.musicDir)

    def get_song_tree(self, directory, dirName=None):

        if dirName:
            tree = {0 : dirName}
        else:
            tree = {0: "root"}

        dirList = os.listdir(directory)
        firstSong = True

        for i, d in enumerate(dirList):
            if os.path.isdir(directory+"/"+d):
                tree[d] = self.get_song_tree(directory+"/"+d, dirName=d)
            elif d.endswith(".mp3"):
                if firstSong:
                    tree["songs"] = [dirName]
                    firstSong = False
                tree["songs"].append(d.split(".")[0])
        return tree

class Dir_List(List_Manager):

    def __init__(self, rootDir, directory):
        super(Dir_List, self).__init__(rootDir)
        self.rootDir = rootDir
        self.directory = directory

    def get_list(self, tree=None, firstCall=True, found=False):

        if firstCall:
            tree = self.songTree
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

class Playlist():

    def __init__(self, rootDir, directory, shuffle = False):
        self.dirList = Dir_List(rootDir, directory).get_list()
        self.directory = rootDir
        if self.dirList != None:
            self.name = self.dirList[0]
        else:
            self.name = "Unknown"
        self.shuffle = shuffle
        self.list = self.makePlaylist(self.dirList, self.directory)

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
                        print(l[0])
                        s, p = self.makePlaylist(l[item], path+"/"+l[0])
                        songList.extend(s)
                        pathList.extend(p)
            return songList, pathList
        else:
            return None

playlist = Playlist("../../mp3", "playlist1")
print(playlist.list)
