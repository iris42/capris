from capris.core import run
from capris.runnable import Runnable


class Pipe(Runnable):
    def __init__(self, *commands):
        self.commands = commands

    def append(self, thing):
        self.commands = self.commands + (thing,)
        return self

    def __iter__(self):
        for runnable in self.commands:
            if isinstance(runnable, Pipe):
                for item in runnable:
                    yield item
                continue
            yield tuple(runnable)

    __iadd__ = append
    __lshift__ = append

    def run(self, **kwargs):
        return run(tuple(self), **kwargs)
