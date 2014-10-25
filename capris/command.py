from capris.core import run
from capris.utils import escape, optionify
from capris.runnable import Runnable


class Command(Runnable):
    """
    Create a new command object.

    :param name: The base command, i.e. 'grep'.
    :param arguments: Arguments for the command.
    :param options: Options for the command.
    """
    base = tuple()
    cwd = None

    def __init__(self, name, *arguments, **options):
        self.command = name
        self.arguments = arguments
        self.options = options
        self.env = {}

    def __iter__(self):
        """
        Yields the strings necessary (in proper
        arguments format instead of messy shell
        escapes) to run this command.
        """
        for item in self.base:
            yield item

        yield self.command
        for item in optionify(self.options):
            yield item

        for item in self.arguments:
            yield escape(item)

    @property
    def commands(self):
        """
        Returns a one-value list containing itself
        (the command object).
        """
        return [self]

    @property
    def environ(self):
        """
        Lookup the "inheritance tree" (base commands
        of subcommands) and collects all of the
        environments.
        """
        env = self.base.environ if self.base else {}
        env.update(self.env)
        return env

    def copy(self, arguments, options):
        """
        Copy the current command object, given the
        arguments and options that need to be updated.
        A convenience alias for this method is the
        ``__call__`` method.

        :param arguments: The arguments.
        :param options: The options.
        """
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
        """
        Create a subcommand with the current command
        as it's base (parent).

        :param command: The name of the command.
        """
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
        """
        Run the command, optionally piping *data* to
        it's ``stdin`` and get a response. If *env*
        is not specified, the default ``env`` will be
        used. Similarly, if *cwd* is not specified,
        the default ``cwd`` will be used.

        :param env: Optional, environment.
        :param cwd: Optional, working directory.
        :param data: Optional, data to pipe in.
        """
        return run(
            (tuple(self),),
            env=env or self.environ,
            cwd=cwd or self.cwd,
            data=data,
        )
