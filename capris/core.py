import os
from threading import Thread
from subprocess import Popen, PIPE


class Response(object):
    def __init__(self, process=None):
        self.history = []
        self.env = {}

        self.process = process
        self.command = None
        self.status_code = None

        self.exception = None
        self.std_err = ''
        self.std_out = ''

    def ok(self):
        return self.status_code == 0

    def __repr__(self):
        if self.command:
            return '<Response [%s]>' % (self.command[0])
        return '<Response>'

    def __iter__(self):
        iterable = self.std_out.split('\n')
        length = len(iterable)
        for index, item in enumerate(iterable):
            if not item and index == (length-1):
                break
            yield item

def run_command(command, env=None, data=None, timeout=None, cwd=None):
    environment = dict(os.environ)
    if env:
        environment.update(env)

    response = Response()
    response.command = command
    response.env = environment

    def callback():
        try:
            process = Popen(args=command,
                            env=env,
                            universal_newlines=True,
                            shell=False,
                            stdout=PIPE,
                            stderr=PIPE,
                            stdin=PIPE,
                            bufsize=0,
                            cwd=cwd)
            response.process = process
            response.std_out, response.std_err = process.communicate(data)
            response.status_code = process.wait()
        except Exception as err:
            response.exception = err

    if timeout is not None:
        thread = Thread(target=callback)
        thread.start()

        thread.join(timeout)
        if thread.is_alive():
            response.process.terminate()
            thread.join()
    else:
        callback()
    return response

def run(commands, **kwargs):
    history = []
    data = kwargs.pop('data') if 'data' in kwargs else None

    for command in commands:
        if len(history) != 0:
            data = history[-1].std_out[0:10*1024]

        response = run_command(command, data=data, **kwargs)
        history.append(response)
        if response.exception:
            raise response.exception

    res = history.pop()
    res.history = history
    return res
