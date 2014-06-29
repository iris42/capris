from threading import Lock

class Transaction(object):
    def __init__(self):
        self.history = []
        self.results = []
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

    def reset(self):
        with self.threadlock:
            del self.history[:]
            del self.results[:]
            self.lock = False

    def __enter__(self):
        self.reset()

    def abort(self):
        with self.threadlock:
            self.lock = True
            del self.history[:]

    def execute(self):
        with self.threadlock:
            for obj, runner, args, kwargs in self.history:
                response = runner(obj, *args, **kwargs)
                self.results.append(response)
                if response.status_code != 0:
                    raise RuntimeError( "runnable %s failed" % (repr(obj) ))
        return self.results

    def __exit__(self, *ignored):
        self.reset()

from capris.transaction.wrappers import TransactionCommand
