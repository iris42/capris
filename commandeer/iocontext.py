from commandeer.core import Runnable, run

class IOContext(Runnable):
    def __init__(self, runnable):
        self.runnable = runnable
        self.input_file = None
        self.output_file = None

    def __str__(self):
        return str(self.runnable)

    def __gt__(self, handle):
        self.output_file = handle
        return self

    def __lt__(self, handle):
        self.input_file = handle
        return self

    def run(self, *args, **kwargs):
        if 'data' not in kwargs and self.input_file is not None:
            kwargs['data'] = self.input_file.read()

        response = run(str(self.runnable), *args, **kwargs)
        if self.output_file is not None:
            data = response.std_out
            self.output_file.write(data)

        return response
