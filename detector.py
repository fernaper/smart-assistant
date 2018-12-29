import os
from interaction import Interaction
from pocketsphinx import LiveSpeech, get_model_path
from unidecode import unidecode

model_path = get_model_path()

class Detector():

    _LANGUAGE = {
        'es':('es-es','es-es.lm.bin','es.dict'),
        'en':('en-en','em-en.lm.bin','en.dict')
    }

    def __init__(self, lang='es'):
        if lang not in Detector._LANGUAGE:
            lang = 'es'
        self.lang = lang
        self.interact = Interaction(lang=self.lang)
        self.voice_detector = LiveSpeech(
            verbose = False,
            sampling_rate = 16000,
            buffer_size = 2048,
            no_search = False,
            full_utt = False,
            hmm = os.path.join(model_path, Detector._LANGUAGE[self.lang][0]),
            lm = os.path.join(model_path, Detector._LANGUAGE[self.lang][1]),
            dic = os.path.join(model_path, Detector._LANGUAGE[self.lang][2]),
            #keyphrase = 'forward'
        )

    def run(self):
        self.interact.say_commands()
        for phrase in self.voice_detector:
            self.interact.on_event(phrase.segments(detailed=True))
            if self.interact.is_end():
                break

Detector().run()
