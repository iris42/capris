from capris.core import run, Process
from capris.utils import escape, optionify


class Command(object):
    base = ()

    def __init__(self, name, *arguments, **options):
        self.command = name
        self.arguments = list(arguments)
        self.options = options
        self.env = {}
        self.cwd = None

    def __iter__(self):
        for item in self.base:
            yield item

        yield self.command
        for item in self.arguments:
            yield escape(item)

        for item in optionify(self.options):
            yield item

    @property
    def commands(self):
        return (self,)

    @property
    def environment(self):
        env = {}
        if self.base:
            env = self.base.environment
        env.update(self.env)
        return env

    def subcommand(self, command, arguments=(), options={}):
        cmd = Command(command,
                      *arguments,
                      **options)
        cmd.base = self
        cmd.cwd = self.cwd
        return cmd

    def __call__(self, *arguments, **options):
        self.arguments.extend(arguments)
        self.options.update(options)
        return self

    def __getattr__(self, attribute):
        values = self.__dict__
        if attribute in values:
            return values[attribute]

        attribute = attribute.replace('_', '-')
        return self.subcommand(attribute)

    def run(self, env=None, cwd=None, data=None):
        return run(
            (tuple(self),),
            env=env or self.environment,
            cwd=cwd or self.cwd,
            data=data,
        )
