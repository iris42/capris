from functools import wraps
from capris.transaction.wrappers import TransactionCommand


class Transaction(object):
    def __init__(self):
        self.commands = []

    def command(self, string):
        cmd = TransactionCommand(string)
        cmd.history = self.commands
        return cmd

    @property
    def defined(self):
        return len(self.commands) > 0

    def __getattr__(self, attr):
        values = self.__dict__
        if attr in values:
            return values[attr]

        attr = attr.replace('_', '-')
        return self.command(attr)

    def execute(self, results=None):
        if results is None:
            results = []
        for command, runner, kwargs in self.commands:
            response = runner(command, **kwargs)
            results.append(response)
            if not response.ok():
                message = ("cannot continue: command %r exited with %s"
                           % (command, response.status_code))
                raise RuntimeError(message)
        return results


def transactional(lazy=False):
    def callback(fn):
        transaction = Transaction()

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if lazy and transaction.defined:
                return transaction
            return fn(transaction, *args, **kwargs)
        return wrapper
    return callback
