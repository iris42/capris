from collections import deque
from commandeer.core import Runnable
from commandeer.utils import option_string, which

class Command(Runnable):
    def __init__(self, command, *positional, **options):
        self.command = command
        self.positional = list(positional)
        self.options = options
        self.base_command = None

    @property
    def absolute(self):
        copy = self.copy(self.__class__)
        copy.command = which(self.command)
        return copy

    @property
    def options_string(self):
        return option_string(self.positional, self.options)

    def __str__(self):
        stack = deque((self.command,))
        if self.positional or self.options:
            stack.append(self.options_string)

        if self.base_command is not None:
            stack.appendleft(str(self.base_command))

        return ' '.join(stack)

    def __getattr__(self, attribute):
        values = self.__dict__
        if attribute not in values:
            attribute = attribute.replace('_', '-')
            return self.subcommand(attribute)

        return values[attribute]

    def copy(self, base):
        copy = base(self.command, *self.positional, **self.options)
        copy.base_command = self.base_command
        return copy

    def __call__(self, *args, **kwargs):
        copy = self.copy(self.__class__)
        copy.positional.extend(args)
        copy.options.update(kwargs)
        return copy

    def subcommand(self, command):
        subcommand = self.__class__(command)
        subcommand.base_command = self
        return subcommand
