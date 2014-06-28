from capris.core import run_command

class Runnable(object):
    def run(self, **kwargs):
        if hasattr(self, 'env'):
            env = self.env.copy()
            env.update(kwargs.pop('env') if 'env' in kwargs else {})
            kwargs['env'] = env

        response = run_command(list(self), **kwargs)
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
        return IOStream(self)

from capris.iostream import IOStream
from capris.pipe import Pipe
