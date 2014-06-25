from envoy import run

class Runnable(object):
    def run(self, **kwargs):
        response = run(str(self), **kwargs)
        return response

    def __repr__(self):
        return '<{name} [{string}]>'.format(
                name=self.__class__.__name__,
                string=str(self)
                )

    def __or__(self, other):
        if isinstance(other, Pipe):
            other.append(self)
            return other
        return Pipe(self, other)

    @property
    def iostream(self):
        return IOContext(self)

from commandeer.iocontext import IOContext
from commandeer.pipe import Pipe
