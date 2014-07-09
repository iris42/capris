from threading import Thread
from subprocess import Popen, PIPE

__all__ = ['Response', 'run', 'run_command']


class Response(object):
    status_code = None
    pid = None

    def __init__(self, command, process=None):
        self.history = []
        self.env = {}

        self.process = process
        self.command = command

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
            if not item and index >= maxindex:
                break
            yield item

def setup_response(response, proc, data, timeout, communicate):
    def callback():
        response.pid = proc.pid
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
        return
    callback()


def run_command(command, timeout=None, env=None, data=None, stream=None,
                lazy=False, cwd=None):
    env = {} if env is None else env
    response = Response(command)
    response.env = env

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
    if not lazy:
        setup_response(response=response,
                       proc=proc,
                       data=data,
                       timeout=timeout,
                       communicate=True)

    return response


def run(commands, **kwargs):
    history = []
    data = kwargs.pop('data', None)
    timeout = kwargs.get('timeout', None)
    stream = None

    # reverse spawning recipe:
    #   cat = Popen(['cat'], stdin=PIPE, stdout=PIPE)
    #   grep = Popen(['grep', '.'], stdin=PIPE, stdout=cat.stdin)
    #
    for command in reversed(commands):
        response = run_command(command,
                               stream=stream,
                               lazy=True,
                               **kwargs)
        stream = response.process.stdin
        history.append(response)

    history.reverse()
    history[0].process.communicate(data)

    length = len(history)
    for index, res in enumerate(history, 1):
        setup_response(response=res,
                       proc=res.process,
                       data=None,
                       timeout=timeout,
                       communicate=(index == length))

    response = history.pop()
    response.history = history
    return response
