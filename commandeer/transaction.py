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


class TransactionCommand(TransactionRunnable, Command):
    def run(self, *args, **kwargs):
        self.history.append((self, Command.run, args, kwargs))

    def copy(self, base):
        copy = Command.copy(self, TransactionCommand)
        copy.history = self.history
        return copy


class TransactionPipe(TransactionRunnable, Pipe):
    def run(self, *args, **kwargs):
        self.history.append((self, Pipe.run, args, kwargs))


class TransactionIOContext(TransactionRunnable, IOContext):
    def run(self, *args, **kwargs):
        self.history.append((self, IOContext.run, args, kwargs))


class Transaction(object):
    def __init__(self):
        self.history = []
        self.results = {}

    def __getattr__(self, command):
        values = self.__dict__
        if command in values:
            return values[command]
        command = self.command(command)
        return command

    def command(self, command):
        command = TransactionCommand(command.replace('_','-'))
        command.history = self
        return command

    def append(self, thing):
        self.history.append(thing)

    def __enter__(self):
        self.history = []
        self.results = []

    def __exit__(self, *ignored):
        for command, runner, args, kwargs in self.history:
            self.results.append(runner(command, *args, **kwargs))
