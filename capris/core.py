from subprocess import Popen, PIPE
from collections import deque


class Response(object):
    def __init__(self, command, proc, pid, status, stdout, stderr):
        self.command = command
        self.proc = proc
        self.pid = pid
        self.status = status
        self.stdout = stdout
        self.stderr = stderr
        self.history = []

    def __repr__(self):
        if not self.command:
            return '<Response>'
        return '<Response [%s]>' % (self.command[0])

    def ok(self, allowed=(0,)):
        return self.status in allowed


class Process(object):
    def __init__(self, args, cwd, env, data):
        self._subprocess = None
        self.args = args
        self.data = data
        self.cwd = cwd
        self.env = env
        self.stdin = PIPE
        self.stdout = PIPE
        self.stderr = PIPE

    def __repr__(self):
        return '<Process [%s]>' % (' '.join(self.args))

    @property
    def subprocess(self):
        if self._subprocess:
            return self._subprocess
        self._subprocess = Popen(
            args=self.args,
            stdin=self.stdin,
            stdout=self.stdout,
            stderr=self.stderr,
            universal_newlines=True,
            cwd=self.cwd,
            env=self.env,
        )
        return self._subprocess

    def run(self):
        proc = self.subprocess
        stdout, stderr = proc.communicate(self.data)
        return Response(
            command=self.args,
            pid=proc.pid,
            proc=self,
            status=proc.wait(),
            stdout=stdout,
            stderr=stderr,
        )


def run(commands, cwd=None, env=None, data=None):
    history = deque()
    previous_stdin = PIPE

    for item in reversed(commands):
        process = Process(args=item, cwd=cwd, env=env, data=None)
        process.stdout = previous_stdin
        history.appendleft(process)
        previous_stdin = process.subprocess.stdin

    history[0].data = data
    responses = [proc.run() for proc in history]

    r = responses.pop()
    r.history = responses
    return r
