from capris.runnable import Runnable


class IOStream(Runnable):
    input = None
    output = None

    def __init__(self, runnable):
        self.runnable = runnable

    def __gt__(self, other):
        self.output = other
        return self

    def __lt__(self, other):
        self.input = other
        return self

    def run(self, **kwargs):
        if 'data' not in kwargs and self.input is not None:
            kwargs['data'] = self.input.read()

        response = self.runnable.run(**kwargs)
        if self.output is not None:
            self.output.write(response.stdout)
        return response
