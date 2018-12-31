from gtts import gTTS
from subprocess import DEVNULL, STDOUT, check_call
from utils import cls
import os
import pygame
cls()

class Music():
    def __init__(self, autoplay=True):
        pygame.init()
        self.set_song()
        if autoplay:
            self.play()

    def __del__(self):
        pygame.quit()

    def set_volume(self, volume=1):
        pygame.mixer.music.set_volume(volume)

    def volume_up(self, value=0.1):
        pygame.mixer.music.set_volume(min(pygame.mixer.music.get_volume() + value,1))

    def volume_down(self, value=0.1):
        pygame.mixer.music.set_volume(max(pygame.mixer.music.get_volume() - value,0.1))

    def set_song(self, path='music/out_of_my_mind-killrudeRemix.mp3'):
        pygame.mixer.music.load(path)

    def play(self, times=0, volume=0.1):
        if volume:
            pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(times)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

class Speech():
    def __init__(self, text, lang='es'):
        try:
            tts = gTTS(text=text, lang=lang)
            self.filename = 'tmp/current-msg.mp3'
            tts.save(self.filename)
            check_call(['mpg123', 'tmp/current-msg.mp3'], stdout=DEVNULL, stderr=STDOUT)
        except Exception as e:
            pass

    def __delete__(self):
        if self.filename:
            os.remove(self.filename)
