from capris.core import run
from capris.runnable import Runnable

__all__ = ['IOStream']


class IOStream(Runnable):
    def __init__(self, runnable):
        self.runnable = runnable
        self.input_file = None
        self.output_file = None
        self.callbacks = []

    def __str__(self):
        return str(self.runnable)

    def __and__(self, callback):
        self.callbacks.append(callback)
        return self

    def __gt__(self, handle):
        self.output_file = handle
        return self

    def __lt__(self, handle):
        self.input_file = handle
        return self

    def __iter__(self):
        iterable = list(self.runnable)
        if isinstance(iterable[0], tuple):
            for item in iterable:
                yield item
            return
        yield iterable

    def run(self, *args, **kwargs):
        if 'data' not in kwargs and self.input_file is not None:
            kwargs['data'] = self.input_file.read()

        response = run(tuple(self), *args, **kwargs)
        if self.output_file is not None:
            data = response.std_out
            self.output_file.write(data)

        for callback in self.callbacks:
            callback(response)
        return response
