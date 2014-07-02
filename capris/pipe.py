from capris.core import run
from capris.runnable import Runnable

__all__ = ['Pipe']


class Pipe(Runnable):
    def __init__(self, *commands):
        self.commands = list(commands)

    def __str__(self):
        stack = []
        for item in self.commands:
            stack.append(str(item))
        return ' | '.join(stack)

    def run(self, *args, **kwargs):
        return run(tuple(self), *args, **kwargs)

    def __iter__(self):
        for item in self.commands:
            yield tuple(item)

    def append(self, command):
        self.commands.append(command)
        return self

    def remove(self, command):
        self.commands.remove(command)
        return self

    __iadd__ = append
    __isub__ = remove
