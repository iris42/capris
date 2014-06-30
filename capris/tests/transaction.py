from capris.tests import CaprisTest
from capris.transaction import transactional

class TransactionTest(CaprisTest):
    def test_basic(self):
        """
        The @transactional decorator should call the
        decorated function with a transaction object
        as the first argument. The transaction object
        should be ``defined`` once the transactional
        commands are ran. Also assert that the commands
        are not ran when `[command].run` is called.
        """
        @transactional
        def setup(transaction):
            grep = transaction.grep
            assert not grep.run()
            return transaction

        transaction = setup()
        assert transaction.commands
        assert transaction.defined

    def test_pipe(self):
        """
        Transaction object's commands should wrap
        pipe objects properly and have lazy running
        behaviour.
        """
        @transactional
        def setup(transaction, run=False):
            grep = transaction.grep
            echo = transaction.echo
            pipe = echo('pattern') | transaction.cat
            assert not pipe.run()

            if run:
                return transaction.execute()
            return transaction

        transaction = setup()
        assert transaction.defined
        assert setup(run=True)[0].std_out == 'pattern\n'

    def test_iostream(self):
        """
        The transaction object's commands should wrap
        iostream objects and encapsulate them properly
        with subclasses, and run later on.
        """
        @transactional
        def setup(transaction, run=False):
            cat = transaction.cat
            iostream = self.helpers.stringio('pattern') > cat.iostream
            assert not iostream.run()

            if run:
                return transaction.execute()
            return transaction

        transaction = setup()
        assert transaction.defined
        # cat doesn't add a newline
        assert setup(run=True)[0].std_out == 'pattern'

    def test_exception(self):
        """
        Assert that the transaction object should
        throw a RuntimeError if a command exits
        with a nonzero status code.
        """
        @transactional
        def setup(transaction):
            grep = transaction.grep
            grep('pattern').run(data="")
            return transaction

        transaction = setup()
        self.assertRaises(RuntimeError, transaction.execute)

