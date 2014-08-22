======
Capris
======

Capris is a semantically versioned, MIT-licensed Python library
built for writing composable apps that leverage external
programs.

A simple example of writing your own git wrapper, complete
with other command-line utilities that you love and use on
a daily basis:

.. code-block:: python

    >>> from capris import Command
    >>> git, grep = Command('git'), Command('grep')

    >>> pipe = git.log(n=10, pretty="oneline") | grep(r'[a-f0-9]\{40\}', o=None)
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

------------
Installation
------------

.. code-block:: sh

    $ pip install capris

-------------
Documentation
-------------

You can read the documentation at https://pythonhosted.org/capris/.


- Code Health: |Health|
- Maintainer: `Eugene Eeo`_
- License: MIT

.. _Eugene Eeo: https://github.com/eugene-eeo
.. |Health| image:: https://landscape.io/github/eugene-eeo/capris/master/landscape.png
   :target: https://landscape.io/github/eugene-eeo/capris/master
      :alt: Code Health
