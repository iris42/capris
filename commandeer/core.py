import os
import subprocess
import threading
from shlex import split, shlex


class Response(object):
    def __init__(self, process=None):
        self.process = process
        self.command = None
        self.status_code = None
        self.history = []

        self.exception = None
        self.std_err = None
        self.std_out = None

def parse(command):
    splitter = shlex(command)
    splitter.whitespace = '|'
    splitter.whitespace_split = True
    stack = []
    while True:
        token = splitter.get_token()
        if not token:
            break
        stack.append(token)
        continue

    return list(map(split, stack))

def run_command(command, env={}, data=None, timeout=None, cwd=None):
    environment = dict(os.environ)
    environment.update(env)

    response = Response()
    if isinstance(data, unicode):
        data = data.encode()

    def callback():
        try:
            process = subprocess.Popen(
                    args=command,
                    env=environment,
                    universal_newlines=True,
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    bufsize=0,
                    cwd=cwd
                    )
            response.process = process
            response.std_out, response.std_err = process.communicate(data)
            response.status_code = process.returncode
        except Exception as err:
            response.exception = err

    thread = threading.Thread(target=callback)
    thread.start()

    thread.join(timeout)
    if thread.is_alive():
        response.process.terminate()
        thread.join()
    return response

def run(command, **kwargs):
    command = parse(command)
    history = []
    for c in command:
        if len(history):
            data = history[-1].std_out[0:10*1024]

        response = run_command(c, **kwargs)
        history.append(response)

    res = history.pop()
    res.history = history
    return res


class Runnable(object):
    def run(self, **kwargs):
        response = run(str(self), **kwargs)
        return response

    def __repr__(self):
        return '<{name} [{string}]>'.format(
                name=self.__class__.__name__,
                string=str(self)
                )

    def __or__(self, other):
        if isinstance(other, Pipe):
            other.append(self)
            return other
        return Pipe(self, other)

    @property
    def iostream(self):
        return IOContext(self)

from commandeer.iocontext import IOContext
from commandeer.pipe import Pipe
