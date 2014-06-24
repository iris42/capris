from envoy import run
from commandeer.template import substitute_values

class Runnable(object):
    def run(self, values=None, **kwargs):
        string = str(self)
        if values is not None:
            string = substitute_values(string, values)

        response = run(string, **kwargs)
        return response

    def __or__(self, other):
        if isinstance(other, Pipe):
            other += self
            return other
        return Pipe(self, other)

    @property
    def iostream(self):
        return IOContext(self)

from commandeer.command import Command
from commandeer.pipe import Pipe
from commandeer.iocontext import IOContext

__all__ = ['Command','Pipe']
VERSION='0.0.15'
