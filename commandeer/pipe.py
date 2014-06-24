from envoy import run
from commandeer.template import substitute_values

class Pipe(object):
    def __init__(self, *commands):
        self.commands = list(commands)

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

    def __or__(self, other):
        if isinstance(other, Pipe):
            pipe = Pipe(*self.commands)
            for item in other.commands:
                pipe += item
            return pipe
        self.append(other)
        return self

    def run(self, values=None, **kwargs):
        string = str(self)
        if values is not None:
            string = substitute_values(string, values)

        response = run(string, **kwargs)
        return response
