from cStringIO import StringIO
import commandeer
import commandeer.transaction
import unittest

class TransactionTest(unittest.TestCase):
    def test_iostream(self):
        transaction = commandeer.transaction.Transaction()
        with transaction:
            grep = transaction.grep()
            iostream = StringIO('haha') > grep('haha').iostream > StringIO()
            iostream.run()

        assert iostream.output_file.getvalue().strip() == 'haha'

    def test_piping(self):
        transaction = commandeer.transaction.Transaction()
        with transaction:
            git = transaction.git()
            grep = transaction.grep()
            pipe = git(graph=None) | grep('commit')
            pipe.run()

        assert list(map(lambda x: x[0], transaction.history)) == [pipe]

    def test_transaction(self):
        transaction = commandeer.transaction.Transaction()
        with transaction:
            git = transaction.git()
            git.run()

        assert transaction.history == [(git, commandeer.Command.run, (), {})]

class IOStreamTest(unittest.TestCase):
    def test_iostream(self):
        grep = commandeer.Command('grep')
        stream = "input" > grep.iostream > "output"

        assert stream.input_file  == 'input'
        assert stream.output_file == 'output'

class PipeTest(unittest.TestCase):
    def test_pipe(self):
        pipe = commandeer.Pipe()
        pipe += commandeer.Command('ls', l=None)
        pipe += commandeer.Command('grep', 'some-pattern', context=1)

        assert str(pipe) == "ls -l | grep --context='1' 'some-pattern'"

    def test_or_magic(self):
        git = commandeer.Command('git')
        grep = commandeer.Command('grep')

        pipe = git | grep
        assert str(pipe) == 'git | grep'
        assert isinstance(pipe, commandeer.Pipe)

        pipe = commandeer.Pipe(git, grep) | grep
        assert str(pipe) == 'git | grep | grep'
        assert isinstance(pipe, commandeer.Pipe)

class CommandTest(unittest.TestCase):
    def test_subcommand(self):
        git = commandeer.Command('git')
        log = git.log(graph=None, date="relative")

        assert set(str(log).split()) == {"git", "log", "--graph", "--date='relative'"}
        assert str(git) == 'git'

    def test_options(self):
        grep = commandeer.Command('grep')
        grep = grep(e='Hello World', label=None, context=1)

        assert grep.options['-e'] == "Hello World"
        assert grep.options['--label'] is None
        assert grep.options['--context'] == 1

if __name__ == "__main__":
    unittest.main()
