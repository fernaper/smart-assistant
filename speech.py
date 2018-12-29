from gtts import gTTS
from subprocess import DEVNULL, STDOUT, check_call
import os

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
