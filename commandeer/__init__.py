from envoy import run
from commandeer.template import substitute_values

class Runnable(object):
    def run(self, values=None, **kwargs):
        string = str(self)
        if values is not None:
            string = substitute_values(string, values)

        if self.input_file is not None and 'data' not in kwargs:
            kwargs['data'] = open(self.input_file).read()

        response = run(string, **kwargs)
        if self.output_file is not None:
            with open(self.output_file, "wb") as handle:
                handle.write(response.std_out)

        return response

    def __or__(self, other):
        if isinstance(other, Pipe):
            other += self
            return other
        return Pipe(self, other)

    def __lt__(self, filename):
        self.input_file = filename
        return self

    def __gt__(self, filename):
        self.output_file = filename
        return self


from commandeer.command import Command
from commandeer.pipe import Pipe

__all__ = ['Command','Pipe']
VERSION='0.0.13'
