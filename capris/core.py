from threading import Thread
from subprocess import Popen, PIPE

__all__ = ['Response', 'run', 'run_command']


class Response(object):
    def __init__(self, command, process=None):
        self.history = []
        self.env = {}

        self.process = process
        self.command = command
        self.status_code = None

        self.exception = None
        self.std_err = ''
        self.std_out = ''

    def ok(self, *allowed):
        return (self.status_code == 0 or
                self.status_code in allowed)

    def __repr__(self):
        if self.command:
           return '<Response [%s]>' % (self.command[0])
        return '<Response>'

    def __iter__(self):
        iterable = self.std_out.split('\n')
        maxindex = len(iterable) - 1
        for index, item in enumerate(iterable):
            if not item and index == maxindex:
                break
            yield item


def run_command(command, timeout=None, env=None, data=None, stream=None, communicate=True, cwd=None):
    env = {} if env is None else env
    response = Response(command)
    response.env = env

    def callback():
        proc = Popen(args=command,
                     shell=False,
                     env=env,
                     cwd=cwd,
                     universal_newlines=True,
                     stdin=PIPE,
                     stdout=PIPE if stream is None else stream,
                     stderr=PIPE,
                     bufsize=0)
        response.process = proc
        if communicate:
            response.std_out, response.std_err = proc.communicate(data)
            response.status_code = proc.wait()

    if timeout is not None:
        thread = Thread(target=callback)
        thread.start()
        thread.join(timeout)
        if thread.is_alive:
            response.process.terminate()
            thread.join()
    else:
        callback()
    return response


def run(commands, **kwargs):
    history = []
    data = kwargs.pop('data', None)
    stream = None

    for command in reversed(commands):
        response = run_command(command,
                               stream=stream,
                               communicate=False,
                               **kwargs)
        history.append(response)
        stream = response.process.stdin

    history[-1].process.communicate(data)
    history.reverse()

    response = history.pop()
    response.history = history

    proc = response.process
    response.std_out, response.std_err = proc.communicate()
    response.status_code = proc.wait()
    return response
