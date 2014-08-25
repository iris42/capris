from capris.core import run
from capris.runnable import Runnable


class Pipe(Runnable):
    """
    Creates a Pipe object with the given *commands*
    assumed to be runnables.

    :param commands: Positional argument of runnables.
    """
    def __init__(self, *commands):
        self.commands = list(commands)

    def append(self, thing):
        """
        Append some*thing* to the pipe. Mutates the
        pipe internally.

        :param thing: The thing to append.
        """
        self.commands.append(thing,)
        return self

    def __iter__(self):
        for runnable in self.commands:
            if isinstance(runnable, Pipe):
                for item in runnable:
                    yield item
                continue
            yield tuple(runnable)

    def __iadd__(self, other):
        self.commands += other.commands

    def run(self, **kwargs):
        """
        Runs the pipe object and returns a response.
        See :func:``capris.core.run`` for the possible
        keyword arguments.
        """
        return run(tuple(self), **kwargs)
