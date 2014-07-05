from capris.tests import CaprisTest


class CommandTest(CaprisTest):
    def test_env(self):
        """
        Command objects should have immutable ``env``
        attributes and should not be affected by the
        ``env`` keyword argument when calling the
        ``run`` method of runnables. Subcommands should
        also have copies of the original environment.
        """
        grep = self.grep()
        grep.env = {'X': 'y', 'Z': 'a'}

        response = grep.run(env={'X': 'z'})
        assert response.env['X'] == 'z'
        assert grep.env['X'] == 'y'

        sub = grep.sub()
        assert sub.env is not grep.env
        assert sub.env == grep.env

    def test_immutable(self):
        """
        Command objects should essentially be immutable
        because they should be easily composable,
        and provide a certain level of thread safety.
        """
        ls = self.ls

        assert ls.subcommand is not ls.subcommand
        assert ls() is not ls

    def test_absolute(self):
        """
        When the ``Command.absolute`` property is
        invoked the executable of the command copy
        returned should be an absolute path.
        """
        ls = self.ls.absolute
        assert ls.command == '/bin/ls'

    def test_copying(self):
        """
        When subcommands or commands are called
        or subcommands are made, they shouldn't
        be of the same instance and when they are
        called, should be copies of the original.
        The base commands of subcommands shouldn't
        be copies of the original command.
        """
        command = self.grep(option="string")
        x, y = command.log, command.subcommand('log')

        assert x is not y
        assert x.command == y().command
        assert x.base_command == y.base_command

    def test_options(self):
        """
        Test that the command renders the option strings
        properly, by making single letter options into
        flags and others into options, and escaping
        properly.
        """
        command = self.grep(option="string", boolean=False, other=True)
        assert set(str(command).split()) == \
            {'grep', "--option=string", "--boolean=false", "--other=true"}

        command = self.grep('pattern', n=1, o=None)
        assert set(str(command).split()) == \
            {"grep", "-n", "1", "pattern", "-o"}

        command = self.grep('"Hello"')
        assert str(command) == 'grep "Hello"'
