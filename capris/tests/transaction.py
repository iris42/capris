from capris.tests import CaprisTest
from capris.transaction import Transaction

class TransactionTest(CaprisTest):
    def test_abort(self):
        """
        Assert that the ``Transaction.abort`` function will
        lock the transaction object by setting the ``lock``
        attribute and then clear the history.
        """
        transaction = Transaction()
        with transaction:
            grep = transaction.grep()
            for i in range(5):
                grep.run()
            transaction.abort()
            grep.run()

            assert transaction.lock
            assert not transaction.history

    def test_iostream(self):
        """
        Test that the ``TransactionRunnable.iostream`` property
        will run properly and not run the ``Transaction*`` objects
        but instead run a string.
        """
        transaction = Transaction()
        with transaction:
            grep = transaction.grep()
            iostream = self.helpers.stringio('haha') > grep('haha').iostream > self.helpers.stringio()
            iostream.run()

            results = transaction.execute()
            assert transaction.history
            assert iostream.output_file.getvalue() == 'haha\n'

            assert results[-1].std_out == 'haha\n'
            assert results[-1].status_code == 0

    def test_piping(self):
        """
        Assert that the running piped commands will only append
        the pipe object to the transaction history, and not the
        commands contained in the pipe object.
        """
        transaction = Transaction()
        with transaction:
            git = transaction.git()
            grep = transaction.grep()
            pipe = git.log(n=10) | grep('commit')
            pipe.run()

            assert len(transaction.history) == 1

    def test_transaction(self):
        """
        Assert that running a command within a transaction
        without calling the ``Transaction.execute`` function
        will not really run the command.
        """
        transaction = Transaction()
        with transaction:
            git = transaction.git()
            git.run()
            assert transaction.history
