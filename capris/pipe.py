from capris.core import run
from capris.runnable import Runnable


class Pipe(Runnable):
    def __init__(self, *commands):
        self.commands = commands

    def append(self, thing):
        self.commands = self.commands + (thing,)
        return self

    def run(self, **kwargs):
        args = [tuple(x) for x in self.commands]
        return run(args, **kwargs)
