from collections import deque
from commandeer import Runnable
from commandeer.utils import make_options

class Command(Runnable):
    def __init__(self, command, *positional, **options):
        self.command = command
        self.positional = list(positional)
        self.options = options
        self.base_command = None

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        self._options = make_options(options)

    @property
    def options_string(self):
        stack = []
        for key, value in self.options.items():
            string = '{key}'
            if value is not None:
                string = '{key}=\'{value}\''
            string = string.format(key=key, value=value)
            stack.append(string)

        for item in self.positional:
            if not item.startswith('"'):
                item = "'{item}'".format(item=item)
            stack.append(item)
        return ' '.join(stack)

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

    def __call__(self, *args, **kwargs):
        copy = Command(self.command, *self.positional)
        copy.base_command = self.base_command
        copy.positional.extend(args)

        copy.options.update(self.options.copy())
        copy.options.update(make_options(kwargs))
        return copy

    def subcommand(self, command):
        subcommand = Command(command)
        subcommand.base_command = self
        return subcommand
