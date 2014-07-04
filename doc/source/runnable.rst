Runnables
=========

Basic Concept
-------------

Runnables are basically objects in the capris API which have a run method. The base
class Runnable doesn't implement the method by raising a NotImplementedError but all
subclasses are expected to implement the run method, as well as the ``iter`` and
``str`` magic methods. For example::

    class SimpleCommand(Runnable):
        def __init__(self, command):
            self.command = command

        def __iter__(self):
            yield self.command

        def __str__(self):
            return str(self.command)

        def run(self):
            return os.system(self.command)

Common Properties
-----------------

Runnables come in three flavours in the capris API- commands, pipes, and iostreams.
There are some operator overloaded properties for them:

- ``|`` operator
- ``iostream`` property
    - ``>`` operator
    - ``<`` operator
    - ``&`` operator

Basically, to pipe the output of a runnable to another using the capris DSL, you
can use the ``|`` operator, provided that the runnable's run method returns a
``capris.core.Response`` object. For example, the following do the same things::

    echo('pattern') | grep('pattern')
    Pipe(echo('pattern'), grep('pattern'))

Starting from Capris ``0.0.72`` the ``|`` operator is guaranteed to not mutate
``Pipe`` objects. To mutate them you can use the += operator of pipe objects or
the ``append`` method, for example::

    pipe = Pipe(command)
    pipe += other_1
    pipe.append(other_2)


The ``iostream`` property returns an IOStream object for the runnable that you
can hook callbacks or redirect files to, for example to do the following in
``capris``::

    $ cat file.txt > echo

We can do either of the following, which are both equivalent but the ``iostream``
variant reduces the overhead because one less process needs to be spawned. Note
that the second variant will mutate the ``iostream`` instance::

    cat('file.txt') | echo
    open('file.txt') > echo.iostream

To redirect the output to another file-like object we need to use the ``>`` operator.
It will mutate the ``iostream`` instance::

    with open('res.txt', 'w') as fp:
        echo('something').iostream > fp
        assert iostream.output_file is fp

To assign callbacks that could be ran after the command has completed execution
succesfully (without raising any exceptions), we can use the & operator, for
example for testing purposes::

    def callback(response):
        assert response.ok()
        assert response.std_out == 'pattern\n'

    echo('something').iostream & callback

Like all the operators overloaded for iostream instances it will mutate the
original instance. You can hook as many callbacks as you like with the register
function, for example::

    iostream = echo('something').iostream
    iostream.register(cb1, cb2, cb3)


The Run Method
--------------

All runnables (defined in the **Capris** API) have a ``run`` method that accepts
keyword arguments to be passed to either the ``run`` or ``run_command`` functions
in the core module. Here is the full `function signature` for those commands:

.. method:: capris.core.run_command(args, env=None, data=None, timeout=None, cwd=None)

    Runs the arguments using ``subprocess.Popen`` and creates and
    returns a ``Response`` object. If timeout is not ``None``, a
    new thread will be created to execute the callback in order
    to be able to enforce the timeout. If an exception was raised
    it will be stored in the ``response.exception`` attribute.

    :param args: An iterable of arguments to be ran.
    :param env:  A dictionary update to the current ``os.environ``.
    :param data: Data to be passed to the stdin of the command.
    :param timeout: Maximum execution time in seconds.
    :param cwd:  The current working directory for the command.

    :returns: A ``Response`` object.

.. method:: capris.core.run(commands, **kwargs)

    Runs all of the commands specified in `commands` argument using
    ``run_command`` and then stores the result in a list. If the
    ``exception`` property of the response wasn't None, it will raise
    it and stop execution. The ``history`` attribute of the response
    will be set to the list of responses (excluding the last command).
    It will automatically pipe the first 24KB of output of the last
    command to the next.

    The 24KB restriction is to avoid broken pipe problems that arise
    when too much data is thrown into stdin. But most of the time
    you shouldn't worry about this restriction- if you are running into
    problems then it should be best practice to use streaming instead
    of in memory solutions.

    :param commands: An iterable of iterables of commands.
    :param kwargs: Keyword arguments to be passed to the ``run_command``
                   function for each command. All options are untouched
                   except for ``data``.

    :returns: A ``Response`` object.

Subclassing
-----------

You can provide your own runnable that can be accepted into parts of the **Capris**
API by subclassing the ``Runnable`` class. You must provide ``run``, ``__iter__``,
and ``__str__`` methods. For example::

    from capris.runnable import Runnable
    from capris.core import run

    class RunnableStack(Runnable):
        def __init__(self, *runnables):
            self.runnables = runnables

        def __iter__(self):
            for item in self.runnables:
                yield item

        def __str__(self):
            return ' && '.join(self)

        def run(self, **kwargs):
            response = run(tuple(self), **kwargs)
            return response

If you do not provide the ``run`` method, it will raise ``NotImplementedError``
whenever you run the runnable object, however that doesn't apply to other magic
methods such as ``__str__`` and ``__iter__``.
