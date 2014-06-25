from envoy import run
from commandeer import Runnable
from commandeer.command import Command
from commandeer.pipe import Pipe
from commandeer.iocontext import IOContext

class TransactionRunnable(Runnable):
    def __or__(self, other):
        if isinstance(other, Pipe):
            other.append(self)
            return other
        pipe = TransactionPipe(self, other)
        pipe.history = self.history
        return pipe

    @property
    def iostream(self):
        iostream = TransactionIOContext(self)
        iostream.history = self.history
        return iostream

    def run(self, *args, **kwargs):
        # assume all classes inherit from their derived
        # ones second
        self.history.append((
            self,
            self.__class__.__bases__[1].run,
            args,
            kwargs
            ))


class TransactionCommand(TransactionRunnable, Command):
    def copy(self, base):
        copy = Command.copy(self, TransactionCommand)
        copy.history = self.history
        return copy


class TransactionPipe(TransactionRunnable, Pipe): pass
class TransactionIOContext(TransactionRunnable, IOContext): pass


class Transaction(object):
    def __init__(self):
        self.history = []
        self.results = []
        self.lock = False

    def __getattr__(self, command):
        values = self.__dict__
        if command in values:
            return values[command]
        command = self.command(command.replace('_','-'))
        return command

    def command(self, command):
        command = TransactionCommand(command)
        command.history = self
        return command

    def append(self, thing):
        if not self.lock:
            self.history.append(thing)

    def __enter__(self):
        self.history = []
        self.results = []
        self.lock = False

    def abort(self):
        self.history = []
        self.lock = True

    def execute(self):
        for command, runner, args, kwargs in self.history:
            response = runner(command, *args, **kwargs)
            self.results.append(response)
            if response.status_code != 0:
                break
        return self.results

    def __exit__(self, *ignored):
        responses = self.execute()
        self.lock = False
        return responses
