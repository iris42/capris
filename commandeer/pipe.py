from commandeer import Runnable

class Pipe(Runnable):
    def __init__(self, *commands):
        self.commands = list(commands)
        self.input_file = None
        self.output_file = None

    def __str__(self):
        stack = []
        for item in self.commands:
            stack.append(str(item))
        return ' | '.join(stack)

    def append(self, command):
        self.commands.append(command)
        return self

    def remove(self, command):
        self.commands.remove(command)
        return self

    __iadd__ = append
    __isub__ = remove
