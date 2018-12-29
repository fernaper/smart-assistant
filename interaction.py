from speech import Speech
from state.AllStates import *
import utils

class Interaction():
    msg = {
        'es': {
            'hi':'Bienvenido al sistema de detección automático Karma.',
            'bye':'Adios vuelve de nuevo.',
            'loading':'Cargando comandos.',
            'cmd': 'Comandos disponibles ',
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
            'com':'is-cmd',
            'ayuda':'help'
        }
    }

    reverse_commands = {lang:{v:k for k,v in c.items()} for lang, c in commands.items()}

    def __init__(self, lang='es', talk=True):
        self.state = ReadyState()
        self.talk = talk
        if lang not in Interaction.msg:
            self.lang = 'es'
        else:
            self.lang = lang
        self.read_msg('hi')
        self.read_msg('loading')

    def __del__(self):
        self.read_msg('bye')

    def cmd(self):
        return self.state.cmd()

    def say_commands(self):
        self.read_msg('{}: {}'.format(Interaction.msg[self.lang]['cmd'],
            ', '.join([Interaction.reverse_commands[self.lang][x] for x in self.cmd()]) +
            ', ' + Interaction.reverse_commands[self.lang]['help']), literal=True)

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

    def on_event(self, event):
        event = [(utils.remove_accents(e[0]),e[1]) for e in event if not utils.tag(e[0])]
        print(' '.join([e[0] for e in event]))
        event = list(filter(lambda x: x[0] != None,
                            [e for e in event
                            if Interaction.commands[self.lang].get(e[0]) in self.cmd()
                            or e[0] == Interaction.reverse_commands[self.lang]['help']]))
        if event:
            event = max(event,key=lambda item:item[1]) # I ordered by confidence
            if event[0] == Interaction.reverse_commands[self.lang]['help']:
                self.say_commands()
                return
            self.read_msg('{}: {}'.format(Interaction.msg[self.lang]['you-say'], event[0]), literal=True)
            self.state = self.state.on_event(Interaction.commands[self.lang].get(event[0]))
            print(self.state)
