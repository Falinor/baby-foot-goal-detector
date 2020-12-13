import glob
import time

from os.path import join
from itertools import cycle


class Sound:
    def __init__(self, path):
        self.path = path
        # self.sound = music.load(path)

    def play(self):
        print('Playing', self.path)
        pass

    def stop(self):
        pass

class Playlist:
    def __init__(self, directory):
        self.songs = glob(join(directory, "*.mp3"))

    def next(self):
        return cycle(self.songs)

