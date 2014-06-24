import commandeer
import unittest

class MainTest(unittest.TestCase):
    def test_options(self):
        grep = commandeer.Command('grep')
        grep(e='Hello World', label=None, context=1)

        assert grep.options['-e'] == "Hello World"
        assert grep.options['--label'] is None
        assert grep.options['--context'] == 1

if __name__ == "__main__":
    unittest.main()
