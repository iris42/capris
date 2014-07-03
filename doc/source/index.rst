.. Capris documentation master file, created by
   sphinx-quickstart on Thu Jul  3 12:59:20 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome
=======

**Capris** is a DSL for building programs that leverage
the subprocess interface, licensed under the MIT license.

A taste of what using **Capris** looks like for bulding
a simple git wrapper, along with all the unix utilities
that you know and love:

.. code-block:: python

    >>> from capris import Command
    >>> git, grep = Command('git'), Command('grep')

    >>> pipe = git.log(n=10, pretty="oneline") | grep(r'[a-f0-9]\{40\}', o=None)
    >>> str(pipe)
    'git log -n 10 --pretty=oneline | grep -o [a-f0-9]\{40\}'

    >>> response = pipe.run()
    >>> response.status_code
    0
    >>> print response.std_out
    ...

Contents
========

.. toctree::
    :maxdepth: 2

    tutorial.rst
    runnable.rst
    transaction.rst
