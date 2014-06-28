from collections import deque
from capris.runnable import Runnable
from capris.utils import option_string, which

class Command(Runnable):
    def __init__(self, command, *positional, **options):
        self.command = command
        self.positional = list(positional)
        self.options = options
        self.base_command = None
        self.env = {}

    @property
    def absolute(self):
        copy = self.copy()
        copy.command = which(self.command)
        return copy

    def __str__(self):
        stack = [self.command]
        if self.positional or self.options:
            stack.extend(option_string(self.positional, self.options))

        if self.base_command is not None:
            newstack = [str(self.base_command)]
            for item in stack:
                newstack.append(item)
            stack = newstack

        return ' '.join(stack)

    def __getattr__(self, attribute):
        values = self.__dict__
        if attribute not in values:
            attribute = attribute.replace('_', '-')
            return self.subcommand(attribute)

        return values[attribute]

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
