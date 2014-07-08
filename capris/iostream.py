from capris.core import run, run_command
from capris.runnable import Runnable
from capris.pipe import Pipe

__all__ = ['IOStream']


class IOStream(Runnable):
    input_file = None
    output_file = None

    def __init__(self, runnable):
        self.runnable = runnable
        self.callbacks = []

    def __lt__(self, fp):
        self.input_file = fp
        return self

    def __gt__(self, fp):
        self.output_file = fp
        return self

    def __and__(self, method):
        self.register(method)
        return self

    def register(self, *methods):
        for item in methods:
            self.callbacks.append(item)

    def __iter__(self):
        for item in self.runnable:
            yield item

    def __str__(self):
        return str(self.runnable)

    def run(self, **kwargs):
        if 'data' not in kwargs and self.input_file:
            kwargs['data'] = self.input_file.read()

        method = run_command
        if isinstance(self.runnable, Pipe):
            method = run

        response = method(tuple(self.runnable), **kwargs)
        if self.output_file:
            self.output_file.write(response.std_out)

        for item in self.callbacks:
            item(response)
        return response
