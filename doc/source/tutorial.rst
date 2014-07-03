Capris Tutorial
===============

By the end of this tutorial you should have a decent idea
behind **Capris**'s philosophy and why it does things in
a certain way, as well as how to do common tasks using the
library.


Installation
------------

To install the latest release version, you can simply::

    $ pip install capris

Else if you want to install the latest development version
it is recommended that you pull and clone the latest git
repository, for example::

    $ git clone ssh://git@github.com/eugene-eeo/capris
    $ cd capris
    $ pip install --editable .

If you want to run the tests suite you can execute the
following command (substitute ``python`` with your version
of Python, i.e. ``python3``)::

    $ python -m capris.tests


Running your first command
--------------------------

Start a new REPL instance and import the ``capris``
library, you should be able to do the following::

    >>> from capris import Command
    >>> echo = Command('echo')

Once we defined our ``echo`` variable we can then
call it with the command line options/flags required,
in this case we'll just echo a simple string, and
store the response::

    >>> response = echo('Hello World!')
    >>> print(response.std_out)
    Hello World!

Notice that the stdout of the command is stored in
the ``response`` object as the ``std_out`` attribute,
which you can then manipulate/use. Similarly, the
`std_err` attribute contains the contents of stderr.

A few other attributes of the ``response`` object
are also available, for an exhaustive list::

    >>> response.env
    {...}
    >>> response.status_code
    0
    >>> response.history
    []
    >>> response.exception
    None
    >>> response.process
    <subprocess.Popen object at 0x...>
    >>> response.command
    'echo'

Very frequently we check for whether the command
has executed properly by determining if it has
exited with a zero exit code. We can do that too
with capris, but the `response` object has a
special convenience method::

    >>> response.ok()
    True

This will definitely help with testing applications
due to the extremely readable code that you can
write.


Piping Stuff Around
-------------------

In the shell you have a very convenient piping
syntax, for example::

    $ git log | grep pattern

The **Capris** DSL also has a similar feature, but
implemented using operator overloading. For example
consider the translation of the previous code block
into Python with the **Capris** DSL::

    >>> git.log | grep('pattern')
    <Pipe [git log | grep pattern]>

Note that neither the ``git`` or ``grep`` commands
are mutated, but a new ``Pipe`` object is created.
The pipe object allows you to pipe the output of
commands to one another in sequence. You can also
programmatically build up the ``Pipe`` object::

    >>> pipe = capris.Pipe()
    >>> pipe += command

Or alternatively if you prefer using methods, you
can call the ``append`` method and pass a pipe
object into a function which expects an object
with an ``append`` method::

    >>> pipe.append(command)

You can also pipe pipes to one another. For a
very simple example, using the syntactic sugar::

    >>> pipe | echo
    <Pipe [git log | grep pattern | echo]>

Note that using the ``|`` operator will always
create a new pipe to allow for easy composability
of commands. Sometimes this is undesirable and
you may need to use the ``append`` method or
the ``+=`` operator to mutate the pipe.

Similar to the `Command` class, you can run the
pipe object using the `run` method.


IO Redirection
--------------

In the shell we often redirect file contents into
the stdin and redirect the stdout of a command into
another file, for example::

    $ file.txt > echo > copy.txt

You can also do that easily using the **Capris** DSL,
although it is more involved due to the need for
`correctness` in the API. But basically to redirect::

    >>> iostream = echo.iostream
    >>> open('file.txt') > iostream > open('copy.txt', 'w')
    >>> iostream.run()

Notice that the ``>`` and ``<`` operators **will**
mutate the iostream object. If you do not want this
behaviour you should create a new iostream object
by using the ``iostream`` property.


Small Quirks
------------

To pass data to stdin, you can use the ``data``
keyword argument (it is more readable) and assign
it to a string::

    >>> command.run(data='strings')

This can be an alternative to using a file-like
object like ``StringIO`` to store the string
value. You can also specify a timeout for the
command being ran and updates to the environment,
for example::

    >>> command.run(timeout=5)
    >>> command.run(env={'OPTION':'value'})

If you want to persist the updates to the environment
variables the recommended way is to change the ``env``
attribute, for example::

    >>> command.env = {'OPTION':'value'}

This will ensure that all subcommands will also run
with the updates to the environment variables. Note
that environment variables are not copied from base
command to subcommand. Instead, lookups are made up
the internal command hierarchy. For example, if you
have the following command, you will get the tree
following it::

    git.log.subcommand
    git
     |-- log
          |-- subcommand

