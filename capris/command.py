from capris.core import run
from capris.utils import escape, optionify
from capris.runnable import Runnable


class Command(Runnable):
    base = tuple()
    cwd = None

    def __init__(self, name, *arguments, **options):
        self.command = name
        self.arguments = arguments
        self.options = options
        self.env = {}

    def __iter__(self):
        for item in self.base:
            yield item

        yield self.command
        for item in optionify(self.options):
            yield item

        for item in self.arguments:
            yield escape(item)

    @property
    def commands(self):
        return (self,)

    @property
    def environ(self):
        env = self.base.environ if self.base else {}
        env.update(self.env)
        return env

    def copy(self, arguments, options):
        cmd = Command(
            self.command,
            *(self.arguments + arguments),
            **self.options
        )
        cmd.options.update(options)
        cmd.env.update(self.env)
        cmd.base = self.base
        cmd.cwd = self.cwd
        return cmd

    def __call__(self, *arguments, **options):
        return self.copy(arguments, options)

    def subcommand(self, command):
        cmd = Command(command)
        cmd.base = self
        cmd.cwd = self.cwd
        return cmd

    def __getattr__(self, attribute):
        values = self.__dict__
        if attribute in values:
            return values[attribute]

        attribute = attribute.replace('_', '-')
        return self.subcommand(attribute)

    def run(self, env=None, cwd=None, data=None):
        return run(
            (tuple(self),),
            env=env or self.environ,
            cwd=cwd or self.cwd,
            data=data,
        )
