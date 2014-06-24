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
        pipe += commandeer.Command('grep', 'some-pattern', context=1)
        assert str(pipe) == "ls -l | grep --context='1' 'some-pattern'"

    def test_substitute(self):
        echo = commandeer.Command('echo', n=None)
        response = echo('"$value"').run(values={'value':'Hello!'})

        assert response.std_out == 'Hello!'
        assert str(echo) == 'echo -n "$value"'

    def test_nested_substitute(self):
        echo = commandeer.Command('echo', n=None)
        response = echo('"${user.name}"').run(values={'user':{'name':'Eugene'}})

        assert response.std_out == 'Eugene'
        assert str(echo) == 'echo -n "${user.name}"'

if __name__ == "__main__":
    unittest.main()
