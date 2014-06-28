from capris.tests import CaprisTest


class CommandTest(CaprisTest):
    def test_env(self):
        """
        ``Command.env`` attribute should be copied
        and updated by the ``data`` keyword argument
        passed to the ``Command.run`` function when
        the command is ran.
        """
        grep = self.grep()
        grep.env = {'KEY':'hey!', 'HEY':'true'}
        response = grep.run(env={"KEY":"yo!"})

        # Command.env should be updated
        assert response.env['KEY'] == 'yo!'
        assert response.env['HEY'] == 'true'

        # Command.env should be provided
        response = grep.run()
        assert response.env['KEY'] == 'hey!'

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
        assert set(str(command).split()) == {'grep', "--option=string", "--boolean=false", "--other=true"}

        command = self.grep('pattern', n=1, o=None)
        assert set(str(command).split()) == {"grep", "-n", "1", "pattern", "-o"}

        command = self.grep('"Hello"')
        assert str(command) == 'grep "Hello"'
