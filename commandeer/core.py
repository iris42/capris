import os
import subprocess
import threading
import shlex


class Response(object):
    def __init__(self, process=None):
        self.history = []
        self.env = {}

        self.process = process
        self.command = None
        self.status_code = None

        self.exception = None
        self.std_err = None
        self.std_out = None

    def __repr__(self):
        if self.command:
            return '<Response [%s]>' % (self.command[0])
        return '<Response>'

    def __iter__(self):
        for item in self.std_out.split('\n'):
            yield item

def parse(command):
    splitter = shlex.shlex(command)
    splitter.whitespace = '|'
    splitter.whitespace_split = True
    while True:
        token = splitter.get_token()
        if not token:
            break
        yield shlex.split(token)
        continue

def popen_callback(command, response, env, data, timeout, cwd):
    def closure():
        response.env = env
        try:
            process = subprocess.Popen(
                    args=command,
                    env=env,
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
    return closure

def run_command(command, env={}, data=None, timeout=None, cwd=None):
    environment = dict(os.environ)
    environment.update(env)

    response = Response()
    thread = threading.Thread(target=popen_callback(command, response, environment, data, timeout, cwd))
    thread.start()

    thread.join(timeout)
    if thread.is_alive():
        response.process.terminate()
        thread.join()
    return response

def run(string, **kwargs):
    history = []
    data = kwargs.pop('data') if 'data' in kwargs else None

    for command in parse(string):
        if len(history):
            data = history[-1].std_out[0:10*1024]

        response = run_command(command, data=data, **kwargs)
        response.command = command
        history.append(response)
        if response.exception:
            raise response.exception

    res = history.pop()
    res.history = history
    return res
