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

    def execute(self):
        if self.lock: return []
        with self.threadlock:
            for command, runner, args, kwargs in self.history:
                response = runner(command, *args, **kwargs)
                self.results.append(response)
                if response.status_code != 0:
                    break
        return self.results

    def __exit__(self, *ignored):
        self.reset()

from commandeer.transaction.wrappers import TransactionCommand
