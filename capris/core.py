from subprocess import Popen, PIPE
from collections import deque


class Response(object):
    """
    Creates a response object with the given
    process *proc*, *pid*, *status*, *stdout*
    value, and *stderr* value.

    :param command: The command that was ran.
    :param proc: The process object.
    :param pid: The PID of the process.
    :param stdout: The stdout value.
    :param stderr: The stderr value.
    """
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
        """
        Returns a boolean dictating if the return
        value of the command was *allowed*.

        :param allowed: defaults to `(0,)`, an
            iterable of accepted status codes.
        """
        return self.status in allowed


class Process(object):
    """
    Create a process objec with the given
    *args*, *cwd*, *env*, and *data*.

    :param args: The arguments to run.
    :param cwd: Which directory to run the
        command in.
    :param env: The environment.
    :param data: The data to pipe.
    """
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

    def pipe(self, data):
        """
        Set the internal piped data to *data*.

        :param data: The data to pipe.
        """
        self.data = data

    @property
    def subprocess(self):
        """
        A cached property that creates a
        ``subprocess.Popen`` object once and
        caches it.
        """
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
        """
        Run the internal ``subprocess`` and
        return a response.
        """
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
    """
    Run multiple piped *commands* optionally in *cwd*,
    with environment *env*, and with *data* piped
    in.

    :param cwd: Which directory to run the commands.
    :param env: The environment for each command.
    :param data: The data to pipe in to the first
        command.
    """
    history = deque()
    previous_stdin = PIPE

    for item in reversed(commands):
        process = Process(args=item, cwd=cwd, env=env, data=None)
        process.stdout = previous_stdin
        history.appendleft(process)
        previous_stdin = process.subprocess.stdin

    history[0].pipe(data)
    responses = [proc.run() for proc in history]

    r = responses.pop()
    r.history = responses
    return r
