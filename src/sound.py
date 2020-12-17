from glob import glob
import time
import simpleaudio as audio
from pydub import AudioSegment
from os import getcwd
from os.path import join
from itertools import cycle


# 5 seconds crossfade
CROSSFADE = 5

class Sound:
    def __init__(self, path):
        self.path = path
        self.sound = audio.WaveObject.from_wave_file(path)

    def play(self):
        self.sound = self.sound.play()
        return self
    
    def wait_done(self):
        self.sound.wait_done()
        return self

class Playlist:
    def __init__(self, directory):
        self.songs = glob(join(directory, "*.wav"))

    def next(self):
        songs = [AudioSegment.from_wav(f) for f in self.songs]
        if len(songs) == 0:
          raise FileNotFoundError

        for song in cycle(songs):
            song = song.fade_in(2000).fade_out(3000)
            # We don't want an abrupt stop at the end, so let's do a crossfade
            playlist_length = len(song) / (1000 * 60)
            self.song = song
            print(self.song)
            yield self
    
    def play(self):
        print('Playing song', self.song)
        return audio.play_buffer(
            self.song.raw_data,
            num_channels=self.song.channels,
            bytes_per_sample=self.song.sample_width,
            sample_rate=self.song.frame_rate 
        )
    
    def wait_done(self):
        print('Before wait_done', self.song)
        self.song.wait_done()

if __name__ == '__main__':
    playlist = Playlist(join(getcwd(), 'sounds', 'ambiances'))
    try:
        for song in playlist.next():
            song.play().wait_done()
    except KeyboardInterrupt:
        print('Exit')
