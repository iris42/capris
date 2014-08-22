class Runnable(object):
    commands = ()

    def run(self):
        raise NotImplementedError

    def __or__(self, other):
        return Pipe(*(self.commands + other.commands))

    @property
    def iostream(self):
        return IOStream(self)


from capris.pipe import Pipe
from capris.iostream import IOStream
