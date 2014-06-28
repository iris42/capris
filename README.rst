==========
Commandeer
==========

Commandeer is a MIT-licensed Python library built for writing
composable apps that leverage the command line.

A simple example of writing your own git wrapper, complete
with other command-line utilities that you love and use on
a daily basis:

.. code-block:: python

    >>> from commandeer import Command
    >>> git, grep = Command('git'), Command('grep')

    >>> pipe = git.log(n=10, pretty="oneline") | grep(r'[a-f0-9]\{40\}', o=None)
    >>> str(pipe)
    "git log -n 10 --pretty='oneline' | grep -o '[a-f0-9]\{40\}'"

    >>> response = pipe.run()
    >>> response.status_code
    0
    >>> print response.std_out
    ...

``commandeer`` allows you to write code that just calls commands
and helps you focus on writing the `commands that you need`,
not the code required to handle calling and getting responses
from the commands. ``commandeer`` does all of the mucking around
with strings and escaping for you.


--------
Features
--------

- DSL for command generation
- Support for nested subcommands
- Smart option generation
- Transactions and redirection
- Built in support for pipes
- Thread safety
- Works with both Python 2 and 3


------------
Installation
------------

To install the library you can simply do a ``git clone`` and then
either ``pip install`` locally or do a ``setup.py``. For example:

.. code-block:: bash

    $ git clone ssh://git@github.com/eugene-eeo/commandeer.git
    $ cd commandeer
    $ pip install .
