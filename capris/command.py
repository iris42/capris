from capris.core import run
from capris.utils import escape, optionify
from capris.runnable import Runnable


class Command(Runnable):
    base = ()
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
        env = {}
        if self.base:
            env = self.base.environ
        env.update(self.env)
        return env

    def copy(self, arguments, options):
        opts = self.options.copy()
        opts.update(options)
        cmd = Command(
            self.command,
            *(self.arguments + arguments),
            **opts
        )
        cmd.base = self.base
        cmd.env = self.environ.copy()
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
