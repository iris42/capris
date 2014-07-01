from capris.core import run_command
from capris.runnable import Runnable
from capris.utils import option_iterable, which

__all__ = ['Command']

class Command(Runnable):
    def __init__(self, command, *positional, **options):
        self.command = command
        self.positional = list(positional)
        self.options = options
        self.base_command = None
        self.env = {}

    @property
    def absolute(self, path=None):
        copy = self.copy()
        copy.command = which(self.command, path)
        return copy

    def __iter__(self):
        if self.base_command is not None:
            for item in self.base_command:
                yield item

        yield self.command
        if self.positional or self.options:
            for item in option_iterable(self.positional, self.options):
                yield item

    def run(self, **kwargs):
        env = self.env.copy()
        if 'env' in kwargs:
            env.update(kwargs.pop('env'))
        kwargs['env'] = env

        response = run_command(tuple(self), **kwargs)
        return response

    def __str__(self):
        stack = [self.command]
        if self.positional or self.options:
            stack.extend(option_iterable(self.positional, self.options))

        if self.base_command is not None:
            stack.insert(0, str(self.base_command))

        return ' '.join(stack)

    def __getattr__(self, attribute):
        values = self.__dict__
        if attribute in values:
            return values[attribute]

        attribute = attribute.replace('_', '-')
        return self.subcommand(attribute)

    def copy(self):
        copy = self.__class__(self.command, *self.positional, **self.options)
        copy.base_command = self.base_command
        return copy

    def __call__(self, *args, **kwargs):
        copy = self.copy()
        copy.positional.extend(args)
        copy.options.update(kwargs)
        return copy

    def subcommand(self, command):
        subcommand = self.__class__(command)
        subcommand.base_command = self
        return subcommand
