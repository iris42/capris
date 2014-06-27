try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
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

            transaction.execute()
            assert transaction.history
            assert iostream.output_file.getvalue() == 'haha\n'
            assert transaction.results[-1].std_out == 'haha\n'
            assert transaction.results[-1].status_code == 0

    def test_piping(self):
        transaction = commandeer.transaction.Transaction()
        with transaction:
            git = transaction.git()
            grep = transaction.grep()
            pipe = git.log(n=10) | grep('commit')
            pipe.run()

            assert transaction.history

    def test_transaction(self):
        transaction = commandeer.transaction.Transaction()
        with transaction:
            git = transaction.git()
            git.run()
            assert transaction.history

class IOStreamTest(unittest.TestCase):
    def test_iostream(self):
        grep = commandeer.Command('grep')
        stream = "input" > grep.iostream > "output"

        assert stream.input_file  == 'input'
        assert stream.output_file == 'output'

    def test_callbacks(self):
        grep = commandeer.Command('grep')
        context  = type('', (object,), {'ran':False})
        def callback(response):
            assert response.std_out == 'pattern\n'
            context.ran = True

        stream = StringIO('pattern\n') > grep('pattern').iostream & callback
        stream.run()

        assert stream.callbacks
        assert context.ran

class DataTest(unittest.TestCase):
    def test_data(self):
        grep = commandeer.Command('grep')
        cat = commandeer.Command('cat')
        pipe = grep('World', o=None) | cat
        response = pipe.run(data='Hello World')

        # check that the data was only passed to the
        # first command
        assert response.std_out == 'World\n'
        assert response.status_code == 0

class PipeTest(unittest.TestCase):
    def test_pipe(self):
        pipe = commandeer.Pipe()
        pipe += commandeer.Command('ls', l=None)
        pipe += commandeer.Command('grep', 'some-pattern', context=1)

        assert str(pipe) == "ls -l | grep --context=1 'some-pattern'"

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

    def test_absolute(self):
        ls = commandeer.Command('ls')
        assert str(ls.absolute) == '/bin/ls'

    def test_escaping(self):
        echo = commandeer.Command('echo')
        assert str(echo('"Hello"')) == 'echo \'\\"Hello\\"\''

        wget = commandeer.Command('wget')
        assert str(wget(ssl=False)) == 'wget --ssl=false'
        assert str(wget(l=5)) == 'wget -l 5'

if __name__ == "__main__":
    unittest.main()
