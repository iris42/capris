from commandeer import Runnable
from commandeer.command import Command
from commandeer.iocontext import IOContext

class TransactionCommand(Command):
    def run(self, *args, **kwargs):
        self.history.append((self, Command.run, args, kwargs))

    def copy(self, base):
        copy = Command.copy(self, TransactionCommand)
        copy.history = self.history
        return copy

    @property
    def iostream(self):
        return TransactionIOContext(self)

class TransactionIOContext(IOContext):
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
        command.history = self.history
        return command

    def __enter__(self):
        self.history = []
        self.results = {}

    def __exit__(self, *ignored):
        for command, runner, args, kwargs in self.history:
            self.results[command] = runner(command, *args, **kwargs)
