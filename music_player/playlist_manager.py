import os
from random import shuffle

class Playlist_Manager(object):

    def __init__(self, musicDir):
        self.musicDir = musicDir
        self.songTree = self.get_song_tree(self.musicDir)

    def get_song_tree(self, directory, dirName=None):

        if dirName:
            tree = {0 : dirName}
        else:
            tree = {0: "root"}

        dirList = os.listdir(directory)
        songNr = 1
        for d in dirList:
            if os.path.isdir(directory+"/"+d):
                tree[d] = self.get_song_tree(directory+"/"+d, dirName=d)
            elif d.endswith(".mp3"):
                tree[songNr] = d.split(".")[0]
                songNr +=1
        return tree

class Playlist(Playlist_Manager):

    def __init__(self, musicDir, playlistDir, shuffle = False):
        super(Playlist, self).__init__(musicDir)
        self.playlistDir = playlistDir
        self.shuffle = shuffle
        self.musicDir = musicDir
        self.playlist = self.makePlaylist()

    def makePlaylist(self):
        songList = []
        for playlist in self.songTree:
            if playlist != 0:
                for song in self.songTree[playlist]:
                    if song != 0 and song != "" and self.songTree[playlist][0] == self.playlistDir:
                        songList.append("%s/%s/%s.mp3"
                            %(self.musicDir,playlist,self.songTree[playlist][song]))
        if self.shuffle:
            shuffle(songList)
        return songList
