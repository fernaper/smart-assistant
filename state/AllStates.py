from state.State import State

class ReadyState(State):
    def on_event(self, event):
        if event == 'start':
            return StartState()
        elif event == 'is-start':
            return IsStartState()
        elif event == 'exit':
            return ExitState()
        return self

    def posible_next(self):
        return [StartState(), IsStartState()]

    def cmd(self):
        return ['start', 'exit', 'help']

class StartState(State):
    def on_event(self, event, *args):
        if event == 'exit':
            return ExitState()
        if event == 'cmd': # If well we are sure that you say this command
            return RunningState(args)
        elif event == 'is-cmd':
            return IsCmdState()
        return self

    def posible_next(self):
        return [ExitState(), RunningState(), IsCmdState()]

    def cmd(self):
        return ['exit', 'cmd', 'help']

class IsStartState(State):
    def on_event(self, event):
        if event == 'yes':
            return StartState()
        elif event == 'no':
            return ReadyState()
        return self

    def posible_next(self):
        return [StartState(), ReadyState()]

    def cmd(self):
        return ['yes', 'no', 'help']

class RunningState(State):
    def on_event(self, event):
        print('Executing: {}'.format(event))
        return StartState()

    def posible_next(self):
        return [StartState()]

    def cmd(self):
        return ['help']

class IsCmdState(State):
    def on_event(self, event):
        if event == 'yes':
            return RunningState()
        elif event == 'no':
            return StartState()
        return self

    def posible_next(self):
        return [RunningState(), StartState()]

    def cmd(self):
        return ['yes', 'no', 'help']

class ExitState(State):
    def on_event(self, event):
        return exit()

    def posible_next(self):
        return []

    def cmd(self):
        return ['help']
# End of our states.

if __name__ == '__main__':
    # Just for testing
    state = ReadyState()
    while True:
        print('Next states: ' + ', '.join([str(x) for x in state.posible_next()]))
        event = input('Command: ')
        state = state.on_event(event)
        print('Currrent state: {}'.format(state))
