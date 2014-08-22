from capris.core import run


class Pipe(object):
    def __init__(self, *commands):
        self.commands = commands

    def __or__(self, other):
        return Pipe(*(self.commands + other.commands))

    def append(self, thing):
        self.commands = self.commands + (thing,)
        return self

    def run(self, **kwargs):
        args = [tuple(x) for x in self.commands]
        return run(args, **kwargs)
