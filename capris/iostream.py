class NullStream(object):
    def read(self, data):
        return None

    def write(self, data):
        return None


class IOStream(object):
    input = NullStream()
    output = NullStream()

    def __init__(self, runnable):
        self.runnable = runnable

    def __or__(self):
        raise NotImplementedError

    def __gt__(self, other):
        self.output = other
        return self

    def __lt__(self, other):
        self.input = other
        return self

    def run(self, **kwargs):
        if 'data' not in kwargs:
            kwargs['data'] = self.input.read()

        response = self.runnable.run(**kwargs)
        self.output.write(response.stdout)
        return response
