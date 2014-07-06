======
Capris
======

.. image:: https://landscape.io/github/eugene-eeo/capris/master/landscape.png
   :target: https://landscape.io/github/eugene-eeo/capris/master
      :alt: Code Health

Capris is a MIT-licensed Python library built for writing
composable apps that leverage the command line.

A simple example of writing your own git wrapper, complete
with other command-line utilities that you love and use on
a daily basis:

.. code-block:: python

    >>> from capris import Command
    >>> git, grep = Command('git'), Command('grep')

    >>> pipe = git.log(n=10, pretty="oneline") | grep(r'[a-f0-9]\{40\}', o=None)
    >>> str(pipe)
    "git log -n 10 --pretty=oneline | grep -o [a-f0-9]\{40\}"

    >>> response = pipe.run()
    >>> response.status_code
    0
    >>> print response.std_out
    ...

``capris`` allows you to write code or tests that just calls
commands and helps you focus on writing the `commands that you
need`, not the code required to handle calling and getting
responses from the commands. ``capris`` does all of the mucking
around with strings and escaping for you.


--------
Features
--------

- Built in support for pipes
- DSL for command generation
- Elegant responses and environment variables
- High-level unit tests for all classes
- Safe- ``capris`` doesn't touch the shell
- Smart option generation
- Support for nested subcommands
- Thread safety
- Transactions and redirection
- Works with both Python 2 and 3
- Fast stream based pipelining


------------
Installation
------------

To install Capris, simply:

.. code-block:: bash

    $ pip install capris

-------------
Documentation
-------------

You can read the documentation at https://pythonhosted.org/capris/.
