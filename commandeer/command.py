from envoy import run
from commandeer.pipe import Pipe

class Command(object):
    def __init__(self, command, *positional, **options):
        self.command = command
        self.positional = positional
        self.options = options
        self.base_command = None

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
        stack = []
        for key, value in self.options.items():
            string = '{key}'
            if value is not None:
                string = '{key}=\'{value}\''
            string = string.format(key=key, value=value)
            stack.append(string)

        for item in self.positional:
            stack.append("'{item}'".format(item=item))

        return ' '.join(stack)

    def __str__(self):
        stack = [self.command]
        options = self.options_string
        if options:
            stack.append(options)
        if self.base_command is not None:
            stack.insert(0, str(self.base_command))
        return ' '.join(stack)

    def __getattr__(self, attribute):
        if attribute not in self.__dict__:
            attribute = attribute.replace('_', '-')
            return self.subcommand(attribute)
        return self.__dict__[attribute]

    def __call__(self, *args, **kwargs):
        self.positional = args
        self.options = kwargs
        return self

    def subcommand(self, command):
        subcommand = Command(command)
        subcommand.base_command = self
        return subcommand

    def run(self, **kwargs):
        response = run(str(self), **kwargs)
        return response
