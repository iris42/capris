from capris.core import run
from capris.runnable import Runnable

class Pipe(Runnable):
    def __init__(self, *commands):
        self.commands = list(commands)

    def __str__(self):
        stack = []
        for item in self.commands:
            stack.append(str(item))
        return ' | '.join(stack)

    def run(self, **kwargs):
        return run(list(self) **kwargs)

    def __iter__(self):
        for item in self.commands:
            yield list(item)

    def append(self, command):
        self.commands.append(command)
        return self

    def remove(self, command):
        self.commands.remove(command)
        return self

    __iadd__ = append
    __isub__ = remove
