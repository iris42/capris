from capris.pipe import Pipe
from capris.command import Command
from capris.tests import CaprisTest

class PipeTest(CaprisTest):
    def test_pipe(self):
        """
        Assert basic pipe functionality and that the piping
        is joining the commands together properly.
        """
        pipe = Pipe()
        pipe += Command('ls', l=None)
        pipe += Command('grep', 'some-pattern', context=1)

        assert str(pipe) == "ls -l | grep --context=1 'some-pattern'"

    def test_or_magic(self):
        """
        Assert that when binding pipe objects and commands,
        that a new Pipe instance is created. Also check that
        piping is joining the commands together properly.
        """
        pipe = self.cat | self.grep
        assert str(pipe) == 'cat | grep'
        assert isinstance(pipe, Pipe)

        new_pipe = pipe | self.grep
        assert str(new_pipe) == 'cat | grep | grep'
        assert new_pipe is not pipe
