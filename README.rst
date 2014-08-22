::

    Python                _
       _______ ____  ____(_)__
      / __/ _ `/ _ \/ __/ (_-<
      \__/\_,_/ .__/_/ /_/___/
             /_/ embrace the shell


**Supported Pythons:** 2.6+, 3.2+

Capris is a semantically versioned, MIT-licensed Python library
built for writing composable apps that leverage external
programs. A simple example of writing your own git wrapper,
complete with other command-line utilities that you love and use
on a daily basis:

.. code-block:: python

    from capris import Command
    git, grep = Command('git'), Command('grep')

    pipe = git.log(n=10, pretty="oneline") | grep(r'[a-f0-9]\{40\}', o=None)
    response = pipe.run()
    print response.std_out

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

------------
Contributing
------------

If you want to contribute, we follow the Github workflow, so fork
the repo, work on the code and just make a pull request (make sure
all tests pass beforehand, at least in the last commit of your pull
request). In short:

.. code-block:: sh

    $ git clone ssh://git@github.com/$USERNAME/graphlite.git
    $ cd graphlite
    $ git checkout -b $FEATURE
    $ # hackedy hack hack
    $ py.test tests
    $ git commit -a
    $ git push

Note that we use py.test for testing so if you haven't, make sure
you pip install pytest. But you should.

- **Code Health:** |Health|
- **Maintainer:** `Eugene Eeo`_
- **License:** MIT

.. _Eugene Eeo: https://github.com/eugene-eeo
.. |Health| image:: https://landscape.io/github/eugene-eeo/capris/master/landscape.png
   :target: https://landscape.io/github/eugene-eeo/capris/master
      :alt: Code Health
