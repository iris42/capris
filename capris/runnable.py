__all__ = ['Runnable']


class Runnable(object):
    def run(self):
        raise NotImplementedError

    def __repr__(self):
        return '<%s [%s]>' % (self.__class__.__name__, str(self))

    def __or__(self, other):
        if isinstance(other, Pipe):
            other.append(self)
            return other
        return Pipe(self, other)

    @property
    def iostream(self):
        return IOStream(self)

from capris.iostream import IOStream
from capris.pipe import Pipe
