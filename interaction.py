from speech import Speech
from speech import Music
from state.AllStates import *
import utils
import difflib

def generate_simplified_cmd(commands):
    ans = {}
    for key, value in commands.items():
        ans[key] = {}
        for k, v in value.items():
            simp_k = k[:min(len(k),3)]
            if not ans[key].get(simp_k):
                ans[key][simp_k] = []
            ans[key][simp_k].append(k)
    return ans

class Interaction():
    msg = {
        'es': {
            'hi':'Bienvenido al sistema de detección automático Karma.',
            'bye':'Adios, vuelve de nuevo.',
            'loading':'Cargando comandos.',
            'cmd': 'Comandos disponibles ',
            'phrase': 'Frase',
            'you-say': 'Dijiste',
            'unknown': 'Comando desconocido.'
        }
    }

    commands = {
        'es': {
            'hola':'start',
            'adios':'exit',
            'si':'yes',
            'no':'no',
            'comandos':'cmd',
            'ayuda':'help'
        }
    }

    reverse_commands = {lang:{v:k for k,v in c.items()} for lang, c in commands.items()}

    simplified_commands = generate_simplified_cmd(commands)

    def __init__(self, lang='es', talk=True):
        self.prev_state = None
        self.state = ReadyState()
        self.talk = talk
        if lang not in Interaction.msg:
            self.lang = 'es'
        else:
            self.lang = lang
        self.music = Music()
        self.read_msg('hi')
        self.read_msg('loading')

    def __del__(self):
        self.read_msg('bye')

    def cmd(self):
        return self.state.cmd()

    def say_commands(self):
        self.read_msg('{}: {}'.format(Interaction.msg[self.lang]['cmd'],
            ', '.join([Interaction.reverse_commands[self.lang][x] for x in self.cmd()])), literal=True)

    def is_end(self):
        return str(self.state) == 'ExitState'

    def read_msg(self, msg, literal=False):
        if literal:
            print(msg)
            if self.talk:
                Speech(msg, lang=self.lang)
            return
        if msg not in Interaction.msg[self.lang]:
            print(Interaction.msg[self.lang]['unknown'])
            if self.talk:
                Speech(Interaction.msg[self.lang]['unknown'], lang=self.lang)
        else:
            print(Interaction.msg[self.lang][msg])
            if self.talk:
                Speech(Interaction.msg[self.lang][msg], lang=self.lang)

    def valid_command(self, event):
        if not event:
            return []
        word, confidence = event
        # If we just say exactly the word
        if Interaction.commands[self.lang].get(word) in self.cmd():
            return [(Interaction.commands[self.lang][word], confidence)]
        possible_cmd = []
        simp_word = word[:min(len(word),3)]
        if simp_word in Interaction.simplified_commands[self.lang]:
            possible_cmd = Interaction.simplified_commands[self.lang][simp_word]
        # We intersect
        rly_possible = []
        for each_word in possible_cmd:
            if Interaction.commands[self.lang][each_word] in self.cmd():
                rly_possible.append(each_word)
        # Now if we have some 'rly_possible' i will select the most accurate (if it is better than 90%)
        ans = []
        for entry in rly_possible:
            diff = difflib.SequenceMatcher(a=word.lower(), b=entry.lower()).ratio()
            if diff > 0.9:
                ans.append((Interaction.commands[self.lang][entry],diff))
            print(word,diff)
        return ans

    def on_event(self, event):
        event = [(utils.remove_accents(e[0]),e[1]) for e in event if not utils.tag(e[0])]
        print('{}: {}'.format(Interaction.msg[self.lang]['phrase'],' '.join([e[0] for e in event])))
        event = [self.valid_command(e) for e in event]
        # Flat list
        event = [y for x in event for y in x]
        if event:
            event = max(event,key=lambda item:item[1])[0] # I ordered by confidence
            if Interaction.reverse_commands[self.lang][event] == Interaction.reverse_commands[self.lang]['help']:
                self.say_commands()
                return
            self.read_msg('{}: {}'.format(
                          Interaction.msg[self.lang]['you-say'],
                          Interaction.reverse_commands[self.lang][event]), literal=True)
            prev_state = self.state
            self.state = self.state.on_event(event)
            if prev_state != self.state:
                self.prev_state = prev_state
                self.say_commands()
            print(self.state)
