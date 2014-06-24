import commandeer
import unittest

class MainTest(unittest.TestCase):
    def test_subcommand(self):
        git = commandeer.Command('git')
        log = git.log(graph=None, date="relative")

        assert set(str(log).split()) == {"git", "log", "--graph", "--date='relative'"}
        assert str(git) == 'git'

    def test_options(self):
        grep = commandeer.Command('grep')
        grep(e='Hello World', label=None, context=1)

        assert grep.options['-e'] == "Hello World"
        assert grep.options['--label'] is None
        assert grep.options['--context'] == 1

    def test_pipe(self):
        pipe = commandeer.Pipe()
        pipe += commandeer.Command('ls', l=None)
        pipe += commandeer.Command('grep', 'some-pattern')
        assert str(pipe) == "ls -l | grep 'some-pattern'"

if __name__ == "__main__":
    unittest.main()
