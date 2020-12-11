import glob
from os.path import join
from itertools import cycle
from pydub import AudioSegment
from pydub.playback import play


class Sound:
    def __init__(self, path):
        self.path = path
        self.sound = AudioSegment.from_mp3(path)

    def play(self):
        play(self.sound)

class Playlist:
    def __init__(self, directory):
        self.songs = [
          AudioSegment.from_mp3(mp3_file)
          for mp3_file
          in glob(join(directory, "*.mp3"))
        ]

    def next(self):
        return cycle(self.songs)