class Transaction(object):
    def __init__(self):
        self.history = []
        self.results = []
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

    def __enter__(self):
        self.history = []
        self.results = []
        self.lock = False

    def abort(self):
        self.history = []
        self.lock = True

    def execute(self):
        for command, runner, args, kwargs in self.history:
            response = runner(command, *args, **kwargs)
            self.results.append(response)
            if response.status_code != 0:
                break
        return self.results

    def __exit__(self, *ignored):
        responses = self.execute()
        self.lock = False
        return responses

from commandeer.transaction.wrappers import TransactionCommand
