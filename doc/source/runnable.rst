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
