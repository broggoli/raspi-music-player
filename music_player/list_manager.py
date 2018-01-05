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

        for i, d in enumerate(dirList):
            if os.path.isdir(directory+"/"+d):
                tree[d] = self.get_song_tree(directory+"/"+d, dirName=d)
            elif d.endswith(".mp3"):
                if i == 0:
                    tree = [dirName]
                tree.append(d.split(".")[0])
        return tree

class Dir_List(List_Manager):

    def __init__(self, rootDir, directory):
        super(Dir_List, self).__init__(rootDir)
        self.rootDir = rootDir
        self.directory = directory

        print(self.get_list())

    def get_list(self, tree=None, firstCall=True, found=False):

        if firstCall:
            tree = self.songTree

        if not found:
            for branch in tree:
                if branch > 0:
                    if branch == self.directory:
                        return self.get_list(tree[branch], False, True)
                    if not isinstance(tree[branch], list):
                        return self.get_list(tree[branch], False, False)

        else:
            """print("found")
            if not isinstance(tree, dict):
                for branch in tree:
                    return self.get_list(tree[branch], False, True)
            else:"""
            return tree

dir_list = Dir_List("../../mp3", "playlist1")

class Playlist(List_Manager):

    def __init__(self, musicDir, playlistDir=None, shuffle = False):
        super(Playlist, self).__init__(musicDir)
        self.name = playlistDir
        self.shuffle = shuffle
        self.list = self.makePlaylist(playlistDir)

    def makePlaylist(self, playlistDir):
        songList = []
        for playlist in self.songTree:
            if playlist != 0:
                for song in self.songTree[playlist]:
                    if song != 0 and song != "" and (self.songTree[playlist][0] == playlistDir or playlistDir == None):
                            songPath = "%s/%s.mp3" %(playlist, self.songTree[playlist][song])
                            songList.append(songPath)
        if self.shuffle:
            shuffle(songList)
        return songList
