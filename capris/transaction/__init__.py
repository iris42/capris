from threading import Lock
from capris.transaction.wrappers import TransactionCommand

__all__ = ['Transaction']

class Transaction(object):
    def __init__(self):
        self.history = []
        self.threadlock = Lock()
        self.lock = False

    def __getattr__(self, command):
        values = self.__dict__
        if command in values:
            return values[command]
        command = self.command(command.replace('_','-'))
        return command

    def command(self, command):
        command = TransactionCommand(command)
        command.history = self
        return command

    def append(self, thing):
        with self.threadlock:
            if not self.lock:
                self.history.append(thing)

    def reset(self, delete_history=True):
        with self.threadlock:
            if delete_history:
                del self.history[:]
            self.lock = False

    def __enter__(self):
        self.reset()

    def abort(self):
        with self.threadlock:
            del self.history[:]
            self.lock = True

    def stop(self):
        with self.threadlock:
            self.lock = True

    def execute(self):
        results = []
        for obj, runner, args, kwargs in self.history:
            response = runner(obj, *args, **kwargs)
            results.append(response)
            if response.status_code != 0:
                raise RuntimeError( "runnable %s failed" % (repr(obj) ))
        return results

    def __exit__(self, *ignored):
        self.reset(delete_history=False)
