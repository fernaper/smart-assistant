from speech import Speech
from state.AllStates import *
import utils

class Interaction():
    msg = {
        'es': {
            'hi':'Bienvenido al sistema de detección automático Karma.',
            'bye':'Adios vuelve de nuevo.',
            'loading':'Cargando comandos.',
            'cmd': 'Comandos disponibles: ',
            'activating': 'Sistema activo.',
            'unknown': 'Comando desconocido.'
        }
    }

    commands = {
        'es': {
            'activa':'start',
            'act':'half-start',
            'adios':'exit',
            'si':'yes',
            'no':'no',
            'comandos':'cmd',
            'com':'is-cmd',
            'ayuda':'help'
        }
    }

    reverse_commands = {lang:{v:k for k,v in c.items()} for lang, c in commands.items()}

    def __init__(self, lang='es'):
        self.prev_state = None
        self.state = ReadyState()
        if lang not in Interaction.msg:
            self.lang = 'es'
        else:
            self.lang = lang
        self.update_cmd()

    def update_cmd(self):
        current = str(self.state)
        if current != self.prev_state:
            print(current)
            self.avaible_cmd = [Interaction.reverse_commands[self.lang][x] for x in self.state.cmd()]
            self.prev_state = current

    def cmd(self):
        return self.avaible_cmd

    def is_end(self):
        return str(self.state) == 'ExitState'

    def read_msg(self, msg, literal=False):
        if literal:
            Speech(msg, lang=self.lang)
            return
        if msg not in Interaction.msg[self.lang]:
            Speech(Interaction.msg[self.lang]['unknown'], lang=self.lang)
        else:
            Speech(Interaction.msg[self.lang][msg], lang=self.lang)

    def on_event(self, event):
        event = [(utils.remove_accents(e[0]),e[1]) for e in event if not utils.tag(e[0])]
        print(' '.join([e[0] for e in event]))

        for e in event:
            print ('This is a fucking shit')
            print(Interaction.commands[self.lang].get(e[0]))
            print(self.cmd())
            if Interaction.commands[self.lang].get(e[0]) in self.cmd():
                print('Passed get')

        event = list(filter(lambda x: x[0] != None,
                            [e for e in event
                            if Interaction.commands[self.lang].get(e[0]) in self.cmd()
                            or e[0] == Interaction.reverse_commands[self.lang]['help']]))
        print('Valid words detected: {}'.format(event))
        if event:
            print(event)
            event = max(event,key=lambda item:item[1]) # I pick the one with the higher probability
            if event[0] == Interaction.reverse_commands[self.lang]['help']:
                self.read_msg('cmd')
                self.read_msg(','.join(self.cmd()), literal=True)
                return
            print('Dijiste: {}'.format(event[0]))
            self.state = self.state.on_event(Interaction.commands[self.lang].get(event[0]))
            print(self.state)
            self.update_cmd()
