from commandeer.command import Command
from commandeer.pipe import Pipe
from commandeer.iocontext import IOContext
from commandeer.core import Runnable


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
        # ones first
        self.history.append((
            self,
            self.__class__.__bases__[0].run,
            args,
            kwargs
            ))


class TransactionPipe(TransactionRunnable, Pipe): pass
class TransactionIOContext(TransactionRunnable, IOContext): pass

class TransactionCommand(TransactionRunnable, Command):
    def copy(self, base):
        copy = Command.copy(self, TransactionCommand)
        copy.history = self.history
        return copy

    def subcommand(self, command):
        copy = Command.subcommand(self, command)
        copy.history = self.history
        return copy
