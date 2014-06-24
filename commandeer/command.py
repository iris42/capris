from envoy import run
from contextlib import contextmanager

class Command(object):
    def __init__(self, command, base_command=None, *positional, **options):
        self.command = command
        self.positional = positional
        self.options = options
        self.subcommands = []
        self.base_command = base_command

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, options):
        results = {}
        for key, value in options.items():
            key = key.replace('_', '-')
            option = '--{key}'.format(key=key)
            if len(key) == 1:
                option = '-{key}'.format(key=key)
            results[option] = value
        self._options = results

    @property
    def options_string(self):
        stack = list(self.positional)
        for key, value in self.options.items():
            string = '{key}'
            if value is not None:
                string = '{key}=\'{value}\''
            string = string.format(key=key, value=value)
            stack.append(string)
        return ' '.join(stack)

    def __str__(self):
        stack = [self.command]
        stack.append(self.options_string)
        if self.base_command is not None:
            stack.insert(0, str(self.base_command))
        return ' '.join(stack)

    def __getattr__(self, attribute):
        if attribute not in self.__dict__:
            attribute = attribute.replace('_', '-')
            return self.build_command(attribute)
        return self.__dict__[attribute]

    def __call__(self, *args, **kwargs):
        self.positional = args
        self.options = kwargs
        return self

    def build_command(self, command):
        subcommand = Command(command, base_command=self)
        self.subcommands.append(subcommand)
        return subcommand

    def run(self):
        response = run(str(self))
        return response
